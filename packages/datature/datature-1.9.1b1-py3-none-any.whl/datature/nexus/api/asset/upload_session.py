#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   upload_session.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset Upload Session
"""
# pylint: disable=R1732, R0902, E0203, W0201

import concurrent.futures
import logging
import struct
import tempfile
import threading
from contextlib import ContextDecorator
from os import path
from pathlib import Path
from typing import List, Optional, Union

import crc32c
import cv2
from filetype import filetype

from datature.nexus import config, error
from datature.nexus.api.operation import Operation
from datature.nexus.api.types import OperationStatusOverview
from datature.nexus.client_context import ClientContext, RestContext
from datature.nexus.medical import get_processor
from datature.nexus.models import UploadSession as UploadSessionModel
from datature.nexus.utils import file_signature, utils

logger = logging.getLogger("datature-nexus")


class UploadSession(RestContext, ContextDecorator):
    """Datature Asset Upload Session Class.

    :param client_context: An instance of ClientContext.
    :param groups: A list of group names to categorize the upload. Default is None.
    :param background:
        A flag indicating whether the upload should run in the background. Default is False.
    """

    def __init__(
        self,
        client_context: ClientContext,
        groups: Optional[List[str]] = None,
        background: bool = False,
    ):
        """Initialize the API Resource."""
        super().__init__(client_context)
        self._local = threading.local()

        self._operation = None  # Lazy initialization if needed
        self.assets = []
        self.file_name_map = {}
        self.operation_ids = []

        self.groups = groups if groups is not None else ["main"]
        self.background = background

    @property
    def operation(self):
        """Initialize operation."""
        if self._operation is None:
            self._operation = Operation(self._context)
        return self._operation

    def _init_http_session(self):
        """Initialize local session and retry policy."""

        self._local.http_session = utils.init_gcs_upload_session()

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, exc_val, _exc_tb):
        """Exit function.
        The function will be called if an exception is raised inside the context manager
        """
        if exc_val is not None:
            # Error handling, patch import session status
            logger.warning("Upload session error existed: %s", exc_val)
            raise error.Error(exc_val)

        # check asset length
        if len(self.assets) == 0 and len(self.operation_ids) == 0:
            raise error.Error("Assets to upload is empty")

        # call API to get signed url
        if self.assets:
            response = self._upload_assets()
            self.operation_ids.append(response.op_id)

        if self.background:
            return {"op_ids": self.operation_ids}

        # Wait server finish generate thumbnail
        self.wait_until_done()

        return {"op_ids": self.operation_ids}

    def __len__(self):
        """Over write len function."""
        return len(self.file_name_map)

    def add_path(self, file_path: str, custom_metadata: dict = None, **kwargs):
        """
        Add asset to upload.

        :param file_path: The path of the file to upload.
        :param custom_metadata: A dictionary of custom metadata to attach to the asset.
        :param kwargs: Additional keyword arguments to pass to the API.
        """
        if not path.exists(file_path):
            raise error.Error("Cannot find the Asset file")

        if path.isdir(file_path):
            file_paths = utils.find_all_assets(file_path)
        else:
            file_paths = [file_path]

        # Convert DICOM and NII file to video asset
        processed_files = self._pre_process_medical_file(file_paths, kwargs)

        for processed_file in processed_files:
            self._generate_metadata(
                processed_file.get("filename"),
                processed_file.get("file_path"),
                custom_metadata,
            )
            # check current asset size
            self._check_current_asset_size()

    def add_bytes(
        self, file_bytes: bytes, filename: str, custom_metadata: dict = None, **kwargs
    ):
        """Attach file in bytes to upload session

        :param file_bytes: The bytes of the file to upload.
        :param filename: The name of the file to upload, should include the file extension.
        :param custom_metadata: A dictionary of custom metadata to attach to the asset.
        :param kwargs: Additional keyword arguments to pass to the API.
        """
        file_mime_type = file_signature.get_file_mime_by_signature(file_bytes)

        if file_mime_type is None:
            raise TypeError(f"UnSupported file: {filename}")

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create a temporary file path
        temp_file_path = path.join(temp_dir, filename)

        # Write file bytes to the temporary file
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_bytes)

        # Convert DICOM and NII file to video asset
        processed_files = self._pre_process_medical_file([temp_file_path], kwargs)

        for processed_file in processed_files:
            self._generate_metadata(
                processed_file.get("filename"),
                processed_file.get("file_path"),
                custom_metadata,
            )
            # check current asset size
            self._check_current_asset_size()

    def _pre_process_medical_file(self, file_paths: str, options: dict = None):
        """Pre process the file, if medical file convert to MP4 first."""
        pre_processed_medical_file = []

        for file_path in file_paths:
            if file_path.lower().endswith((".dcm", ".nii")):
                processor = get_processor(file_path)

                process_data = {"file": file_path, "options": options}
                processor.valid(process_data)
                resp = processor.process(process_data)

                if resp:
                    # change the converted file_path and filename
                    pre_processed_medical_file = pre_processed_medical_file + [
                        {"filename": Path(file_path).stem, "file_path": file_path}
                        for file_path in resp
                    ]
            else:
                pre_processed_medical_file.append(
                    {"filename": path.basename(file_path), "file_path": file_path}
                )
        return pre_processed_medical_file

    def _generate_metadata(
        self, filename: str, file_path: str, custom_metadata: dict = None
    ):
        """process the file to asset metadata."""
        with open(file_path, "rb") as file:
            contents = file.read()

            # calculate file crc32
            file_hash = crc32c.CRC32CHash()
            file_hash.update(contents)

            # To fix the wrong crc32 caused by mac M1 clip
            crc32 = struct.unpack(">l", file_hash.digest())[0]

            size = path.getsize(file_path)

            mime_kind = filetype.guess(file_path)

            file.close()

            if self.file_name_map.get(filename) is not None:
                raise error.Error(
                    f"Cannot add multiple files with the same name, {filename}"
                )

            if filename and size and crc32 and mime_kind:
                if mime_kind.mime in ["image/jpeg", "image/png"]:
                    asset_metadata = {
                        "filename": filename,
                        "size": size,
                        "crc32c": crc32,
                        "mime": mime_kind.mime,
                        "customMetadata": custom_metadata or {},
                    }
                elif mime_kind.mime == "video/mp4":
                    cap = cv2.VideoCapture(file_path)
                    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                    asset_metadata = {
                        "filename": filename,
                        "size": size,
                        "crc32c": crc32,
                        "mime": mime_kind.mime,
                        "frames": frames,
                        "encoder": {"profile": "h264Saver", "everyNthFrame": 1},
                        "customMetadata": custom_metadata or {},
                    }
                else:
                    raise error.Error("UnSupported asset file")

                self.assets.append(asset_metadata)
                self.file_name_map[filename] = {"path": file_path}

                logger.debug("Add asset: %s", asset_metadata)
            else:
                raise error.Error("UnSupported asset file")

    def _upload_file_thought_signed_url(self, asset_upload):
        filename = asset_upload.get("metadata").get("filename")
        file_path = self.file_name_map.get(filename)["path"]

        # upload asset to GCP
        self._local.http_session.request(
            asset_upload.upload.method,
            asset_upload.upload.url,
            headers=asset_upload.upload.headers,
            data=open(file_path, "rb"),
            timeout=config.REQUEST_TIME_OUT_SECONDS,
        )
        return filename

    def _upload_assets(self):
        """Use ThreadPoolExecutor to upload files to GCP."""
        upload_session_response = self.requester.POST(
            f"/projects/{self.project_id}/assetuploadsessions",
            request_body={"groups": self.groups, "assets": self.assets},
            response_type=UploadSessionModel,
        )

        # Use ThreadPoolExecutor to upload files in parallel
        with concurrent.futures.ThreadPoolExecutor(
            initializer=self._init_http_session
        ) as executor:
            # Submit tasks to the executor
            futures = [
                executor.submit(self._upload_file_thought_signed_url, asset_upload)
                for asset_upload in upload_session_response.assets
            ]

            # Optionally, you can handle the results of the uploads here
            for future in futures:
                filename = future.result()

                logger.debug("Finished Uploading: % s", filename)

            logger.debug("All files uploaded")

        return upload_session_response

    def wait_until_done(
        self,
        raise_exception_if: Union[
            OperationStatusOverview, str
        ] = OperationStatusOverview.ERRORED,
    ):
        """
        Wait for all operations to be done.
        This function only works when background is set to False.
        It functions the same as Operation.wait_until_done.

        :param raise_exception_if: The condition to raise error.
        :return: The operation status metadata if the operation has finished,
        """
        assert isinstance(raise_exception_if, (str, OperationStatusOverview))

        if isinstance(raise_exception_if, str):
            raise_exception_if = OperationStatusOverview(raise_exception_if)

        if len(self.operation_ids) == 0:
            logger.debug("All operations finished")
            return True

        # Use ThreadPoolExecutor to upload files in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            futures = [
                executor.submit(
                    self.operation.wait_until_done,
                    op_id,
                    raise_exception_if=raise_exception_if,
                )
                for op_id in self.operation_ids
            ]

            # Optionally, you can handle the results of the uploads here
            for future in futures:
                res = future.result()

                logger.debug("Finished operation: % s", res)

            logger.debug("All operations finished")
        return True

    # check current asset size

    def _check_current_asset_size(self):
        if len(self.assets) >= config.ASSET_UPLOAD_SESSION_BATCH_SIZE:
            upload_operation = self._upload_assets()

            self.operation_ids.append(upload_operation.op_id)
            # clear current batch
            self.assets = []

    def get_operation_ids(self):
        """
        A list of operation IDs. Because some dependency limits,
        each operation allows a maximum of 5000 assets.
        So if the total number of assets goes up over 5000,
        it will return a list of operation IDs.

        If you want to control the operations manually,
        you can use this function to get the operation ids.
        And the call project.operation.wait_until_done or project.operation.get
        to wait for the operations to finish.

        :return: A list of operation ids.

        :example:
            .. code-block:: python

                ['op_1', 'op_2', 'op_3']

        """
        return self.operation_ids
