#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   asset.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset API
"""

from typing import List, Optional, Union

from datature.nexus import models
from datature.nexus.api.asset.upload_session import UploadSession
from datature.nexus.api.operation import Operation
from datature.nexus.api.types import AssetFilter, AssetMetadata, Pagination
from datature.nexus.client_context import ClientContext, RestContext


class Asset(RestContext):
    """Datature Annotation API Resource."""

    def __init__(self, client_context: ClientContext):
        """Initialize the API Resource."""
        super().__init__(client_context)
        self.operation = Operation(client_context)

    def list(
        self,
        pagination: Union[Pagination, dict, None] = None,
        filters: Union[AssetFilter, dict, None] = None,
    ) -> models.PaginationResponse[models.Asset]:
        """Retrieves a list of all assets in the project.

        :param pagination: A dictionary containing the limit of
                            the number of assets to be returned in each page (defaults to 100),
                            and the page cursor for page selection (defaults to the first page).
        :param filters: A dictionary containing the filters of
                            the assets to be returned.
        :return: A msgspec struct of pagination response with the following structure:

                .. code-block:: python

                    PaginationResponse(
                        next_page='T2YAGDY1NWFlNDcyMzZkiMDYwMTQ5N2U2',
                        prev_page=None,
                        data=[
                            Asset(
                                id='asset_8208740a-2d9c-46e8-abb9-5777371bdcd3',
                                filename='boat180.png',
                                project='proj_cd067221d5a6e4007ccbb4afb5966535',
                                status='None',
                                create_date=1701927649302,
                                url='',
                                metadata=AssetMetadata(
                                    file_size=186497,
                                    mime_type='image/png',
                                    height=243,
                                    width=400,
                                    groups=['main'],
                                    custom_metadata={'captureAt': '2021-03-10T09:00:00Z'}
                                ),
                                statistic=AssetAnnotationsStatistic(
                                    tags_count=[],
                                    total_annotations=0
                                )
                            )
                        ]
                    )

        :example:
                .. code-block:: python

                        from datature.nexus import Client

                        project = Client("5aa41e8ba........").get_project("proj_b705a........")

                        project.assets.list({
                            "limit": 2,
                            "page": "ZjYzYmJkM2FjN2UxOTA4ZmU0ZjE0Yjk5Mg"
                        }, filters={
                            "status": "Annotated",
                            "groups": ["main"],
                        })

                        # or
                        project.assets.list(
                            nexus.ApiTypes.Pagination(
                                limit= 2,
                                page="ZjYzYmJkM2FjN2UxOTA4ZmU0ZjE0Yjk5Mg"
                            ),
                            filters=nexus.ApiTypes.AssetFilter(status="Annotated", groups=["main"])
                        )

        """
        assert isinstance(pagination, (Pagination, dict, type(None)))
        assert isinstance(filters, (AssetFilter, dict, type(None)))

        if isinstance(pagination, dict):
            pagination = Pagination(**pagination)
        if pagination is None:
            pagination = Pagination()

        if isinstance(filters, dict):
            filters = AssetFilter(**filters)
        if filters is None:
            filters = AssetFilter()

        return self.requester.GET(
            f"/projects/{self.project_id}/assets",
            query={**pagination.to_json(), **filters.to_json()},
            response_type=models.PaginationResponse[models.Asset],
        )

    def get(self, asset_id_or_name: str) -> models.Asset:
        """Retrieves a specific asset using the asset ID or file name.

        :param asset_id_or_name: The ID or file name of the asset as a string.
        :return: A msgspec struct containing the metadata of one asset with the following structure:

                .. code-block:: python

                        Asset(
                            id='asset_8208740a-2d9c-46e8-abb9-5777371bdcd3',
                            filename='boat180.png',
                            project='proj_cd067221d5a6e4007ccbb4afb5966535',
                            status='None',
                            create_date=1701927649302,
                            url='',
                            metadata=AssetMetadata(
                                file_size=186497,
                                mime_type='image/png',
                                height=243,
                                width=400,
                                groups=['main'],
                                custom_metadata={'captureAt': '2021-03-10T09:00:00Z'}
                            ),
                            statistic=AssetAnnotationsStatistic(
                                tags_count=[],
                                total_annotations=0
                            )
                        )

        :example:
                .. code-block:: python

                        from datature.nexus import Client

                        project = Client("5aa41e8ba........").get_project("proj_b705a........")
                        project.assets.get("asset_6aea3395-9a72-4bb5-9ee0-19248c903c56")
        """
        assert isinstance(asset_id_or_name, str)
        return self.requester.GET(
            f"/projects/{self.project_id}/assets/{asset_id_or_name}",
            response_type=models.Asset,
        )

    def update(
        self, asset_id_or_name: str, asset_meta: Union[AssetMetadata, dict]
    ) -> models.Asset:
        """Updates the metadata of a specific asset.

        :param asset_id_or_name: The ID or file name of the asset as a string.
        :param asset_meta: The new metadata of the asset to be updated.
        :return: A msgspec struct containing the metadata of one asset with the following structure:

                .. code-block:: python

                        Asset(
                            id='asset_f4dcb429-0332-4dd6-a1b4-fee794031ba6',
                            project_id='proj_cd067221d5a6e4007ccbb4afb5966535',
                            filename='boat194.png',
                            status='None',
                            create_date=1701927649302,
                            url='',
                            metadata=AssetMetadata(
                                file_size=172676,
                                mime_type='image/png',
                                height=384,
                                width=422,
                                groups=['main'],
                                custom_metadata={'captureAt': '2021-03-10T09:00:00Z'}
                            ),
                            statistic=AssetAnnotationsStatistic(
                                tags_count=[],
                                total_annotations=0
                            )
                        )

        :example:
                .. code-block:: python

                        from datature.nexus import Client

                        project = Client("5aa41e8ba........").get_project("proj_b705a........")

                        project.assets.update(
                            "asset_6aea3395-9a72-4bb5-9ee0-19248c903c56",
                            {
                                "status": "Annotated"
                            }
                        )
        """
        assert isinstance(asset_id_or_name, str)
        assert isinstance(asset_meta, (AssetMetadata, dict))

        if isinstance(asset_meta, dict):
            asset_meta = AssetMetadata(**asset_meta)

        return self.requester.PATCH(
            f"/projects/{self.project_id}/assets/{asset_id_or_name}",
            request_body=asset_meta.to_json(),
            response_type=models.Asset,
        )

    def delete(self, asset_id_or_name: str) -> models.DeleteResponse:
        """Deletes a specific asset from the project.

        :param asset_id_or_name: The ID or file name of the asset as a string.
        :return: A msgspec struct containing the
            deleted asset ID and the deletion status with the following structure.

                .. code-block:: python

                    DeleteResponse(deleted=True, id='asset_8208740a-2d9c-46e8-abb9-5777371bdcd3')

        :example:

                .. code-block:: python

                        from datature.nexus import Client

                        project = Client("5aa41e8ba........").get_project("proj_b705a........")

                        project.assets.delete(
                            "asset_6aea3395-9a72-4bb5-9ee0-19248c903c56",
                        )
        """
        assert isinstance(asset_id_or_name, str)
        return self.requester.DELETE(
            f"/projects/{self.project_id}/assets/{asset_id_or_name}",
            response_type=models.DeleteResponse,
        )

    def create_upload_session(
        self, groups: Optional[List[str]] = None, background: bool = False
    ) -> UploadSession:
        """
        Creates a new upload session with specified
        groups and an option to run in the background.

        This method initializes and returns an UploadSession object,
        which can be used to manage file uploads within the system.

        :param groups: A list of group names to categorize the upload. Default is None.
        :param background: A flag indicating whether
                            the upload should run in the background. Default is False.
        :return: UploadSession: An instance of the UploadSession class.
        :example:

                .. code-block:: python

                    from datature.nexus import Client

                    project = Client("5aa41e8ba........").get_project("proj_b705a........")

                    upload_session = project.assets.create_upload_session(
                                                groups=["main"],
                                                background=True
                                            )

                    with upload_session as session:
                        # add assets path to upload session
                        upload_session.add_path(
                            "folder/path/to/files",
                            custom_metadata={"key": "value"}
                        )

                        upload_session.add_bytes(
                            b"bytes/of/file",
                            "filename",
                            custom_metadata={"key": "value"}
                        )
        """
        assert isinstance(groups, (list, type(None)))
        assert isinstance(background, bool)

        return UploadSession(self._context, groups, background)

    def list_groups(self, groups: Union[List[str], None] = None) -> models.AssetGroups:
        """Retrieve asset statistics categorized by asset group and asset status.

        :param groups: A string array of name(s) of asset group(s).
        :return: A list of msgspec struct of
            the categorized asset statistics with the following structure:

                .. code-block:: python

                        [
                            AssetGroup(
                                group='1',
                                statistic=AssetGroupStatistic(
                                    total_assets=1,
                                    annotated_assets=0,
                                    reviewed_assets=0,
                                    to_fixed_assets=0,
                                    completed_assets=0
                                )
                            ),
                            AssetGroup(
                                group='main',
                                statistic=AssetGroupStatistic(
                                    total_assets=503,
                                    annotated_assets=0,
                                    reviewed_assets=0,
                                    to_fixed_assets=0,
                                    completed_assets=0
                                )
                            )
                        ]

        :example:

                .. code-block:: python

                    from datature.nexus import Client

                    project = Client("5aa41e8ba........").get_project("proj_b705a........")
                    project.assets.list_groups()
        """
        assert isinstance(groups, (list, type(None)))

        return self.requester.GET(
            f"/projects/{self.project_id}/assetgroups",
            query={"group": groups},
            response_type=models.AssetGroups,
        )
