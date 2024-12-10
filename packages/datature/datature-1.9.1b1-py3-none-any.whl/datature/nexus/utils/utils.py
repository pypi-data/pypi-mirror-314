#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   utils.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   Utils Class module
"""

import base64
import glob
import os
import secrets
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Union

import dateparser
import pytz
from InquirerPy import inquirer
from InquirerPy.validator import ValidationError, Validator
from requests import Session, request
from requests.adapters import HTTPAdapter, Retry
from wcwidth import wcswidth

from datature.nexus import config, models
from datature.nexus.cli import consts

SUPPORTED_MRI_EXTENSIONS = ["*.dcm", "*.nii"]

SUPPORTED_IMAGE_VIDEO_EXTENSIONS = ["*.jpg", "*.png", "*.jpeg", "*.mp4"]

SUPPORTED_FILE_EXTENSIONS = SUPPORTED_MRI_EXTENSIONS + SUPPORTED_IMAGE_VIDEO_EXTENSIONS

ANNOTATION_FORMAT_EXTENSIONS = ["*.json", "*.csv", "*.xml", "*.labels", "*.txt"]


class NameAndEmptyInputValidator(Validator):
    """Validator for too long name and empty input."""

    MAX_NAME_LENGTH = 120

    def validate(self, document) -> None:
        """
        Validate the input.

        :param document: The input document.
        """
        if not len(document.text) > 0:
            raise ValidationError(
                message="Name cannot be empty.",
                cursor_position=document.cursor_position,
            )

        if len(document.text) > self.MAX_NAME_LENGTH:
            raise ValidationError(
                message=f"Name is too long ({len(document.text)} characters), maximum length is {self.MAX_NAME_LENGTH} characters.",
                cursor_position=document.cursor_position,
            )


class PathAndEmptyInputValidator(Validator):
    """Validator for invalid path and empty input."""

    def validate(self, document) -> None:
        """
        Validate the input.

        :param document: The input document.
        """
        if not len(document.text) > 0:
            raise ValidationError(
                message="Path cannot be empty.",
                cursor_position=document.cursor_position,
            )
        if not Path(document.text).expanduser().resolve().exists():
            raise ValidationError(
                message="Path does not exist, please enter a valid path.",
                cursor_position=document.cursor_position,
            )


class DateTimeValidator(Validator):
    """Validator for invalid datetime format input."""

    def __init__(
        self,
        start_datetime: Optional[datetime] = None,
        timezone: pytz.timezone = pytz.utc,
    ):
        super().__init__()
        self.start_datetime = start_datetime
        self.timezone = timezone

    def validate(self, document) -> None:
        """
        Validate the input.

        :param document: The input document.
        """
        if not len(document.text) > 0:
            return

        try:
            datetime_obj = self.parse(document.text, self.timezone)
        except (ValueError, TypeError) as exc:
            raise ValidationError(
                message=f"Error parsing datetime input: {exc}",
                cursor_position=document.cursor_position,
            ) from exc

        if not datetime_obj:
            raise ValidationError(
                message=(
                    f"Ambiguous or unknown datetime format: {document.text}. Please ensure the datetime "
                    "is in a valid format and is as precise as possible."
                ),
                cursor_position=document.cursor_position,
            )

        # check if time is in the past, with a 1 minute buffer
        if datetime_obj < datetime.now(self.timezone) - timedelta(minutes=1):
            raise ValidationError(
                message="Datetime cannot be in the past. Please enter a future datetime.",
                cursor_position=document.cursor_position,
            )

        # check if time is earlier than a provided datetime
        if self.start_datetime and datetime_obj <= self.start_datetime:
            raise ValidationError(
                message=(
                    f"Datetime must be later than start datetime of "
                    f"{pretty_print_datetime(self.start_datetime, self.timezone)}."
                ),
                cursor_position=document.cursor_position,
            )

    @classmethod
    def parse(
        cls, datetime_string: str = "", timezone: pytz.timezone = pytz.utc
    ) -> Optional[datetime]:
        """
        Parse the datetime string.

        :param datetime_string: The datetime string to parse.
        :param timezone: The timezone to use.
        :return: The parsed datetime object.
        """
        if not datetime_string:
            return None

        datetime_parsed = dateparser.date.DateDataParser(
            languages=["en"],
            settings={
                "TIMEZONE": timezone.zone,
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "RETURN_TIME_AS_PERIOD": True,
            },
        ).get_date_data(datetime_string)

        if not datetime_parsed.date_obj:
            return None

        return datetime_parsed.date_obj.astimezone(timezone)


def find_all_assets(path: str) -> List[str]:
    """
    List all assets under folder, include sub folder.

    :param path: The folder to upload assets.
    :return: assets path list.
    """
    file_paths = []

    # find all assets under folder and sub folders
    for file_ext in SUPPORTED_FILE_EXTENSIONS:
        file_paths.extend(glob.glob(os.path.join(path, "**", file_ext), recursive=True))
    if is_fs_case_sensitive():
        for file_ext in SUPPORTED_FILE_EXTENSIONS:
            file_paths.extend(
                glob.glob(os.path.join(path, "**", file_ext.upper()), recursive=True)
            )

    return file_paths


def find_all_annotations_files(path: str) -> List[str]:
    """
    List all annotations files under folder, include sub folder.

    :param path: The folder to upload annotations files.
    :return: assets path list.
    """
    file_paths = []

    # find all assets under folder and sub folders
    for file_ext in ANNOTATION_FORMAT_EXTENSIONS:
        file_paths.extend(glob.glob(os.path.join(path, "**", file_ext), recursive=True))
    if is_fs_case_sensitive():
        for file_ext in SUPPORTED_FILE_EXTENSIONS:
            file_paths.extend(
                glob.glob(os.path.join(path, "**", file_ext.upper()), recursive=True)
            )

    return file_paths


def get_exportable_annotations_formats(project_type: str) -> List[str]:
    """
    Get the exported annotations formats by project type.

    :param project_type: The type of the project.
    :return: The exported annotations formats.
    """
    if project_type == "Classification":
        return ["csv_classification", "classification_tfrecord"]

    if project_type == "Keypoint":
        return ["keypoints_coco"]

    return [
        "coco",
        "csv_fourcorner",
        "csv_widthheight",
        "pascal_voc",
        "yolo_darknet",
        "yolo_keras_pytorch",
        "createml",
        "tfrecord",
        "polygon_single",
        "polygon_coco",
    ]


def init_gcs_upload_session():
    """
    Initializes an HTTP session for uploading files to
        Google Cloud Storage (GCS) with a configured retry policy.

    The retry policy is configured to retry up to 5 times on specific
        HTTP status codes (500, 502, 503, 504) that commonly represent
        transient server errors. A backoff factor is used to introduce
        a delay between retry attempts.

    Returns:
        Session: A requests Session object configured with the retry policy.
    """
    # Define the retry policy
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

    http_session = Session()
    # Mount the retry policy for HTTP and HTTPS requests
    http_session.mount("http://", HTTPAdapter(max_retries=retries))
    http_session.mount("https://", HTTPAdapter(max_retries=retries))

    return http_session


def get_download_path(path: Union[str, Path] = None) -> Path:
    """
    Gets the download path for storing files.
        If the provided path does not exist, it creates the directory.

    Args:
        path (Union[str, Path], optional):
            The path where files should be downloaded or stored.
            It can be a string or a Path object. If None, the current
            working directory is used.

    Returns:
        Path: The resolved download path as a Path object.
    """
    if path:
        # Check if path is a string and convert it to a Path object if
        # necessary
        download_path = Path(path) if isinstance(path, str) else path

        # Create the directory if it doesn't exist
        download_path.mkdir(parents=True, exist_ok=True)
    else:
        # If path is None, use the current working directory
        download_path = Path.cwd()

    return download_path


def download_files_to_tempfile(signed_url: models.DownloadSignedUrl) -> str:
    """
    Downloads a file from a signed URL to a temporary file.

    Args:
        signed_url (models.DownloadSignedUrl):
            An object containing the signed URL and the HTTP method for the
            request.

    Returns:
        Path: The path to the downloaded temporary file.

    Raises:
        requests.RequestException: If there is an issue with making the
        request.
    """
    method = signed_url.method
    url = signed_url.url

    resp = request(method, url, stream=True, timeout=config.REQUEST_TIME_OUT_SECONDS)

    # Download the file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for data in resp.iter_content(chunk_size=1024):
            temp_file.write(data)

    return temp_file.name


def is_fs_case_sensitive() -> bool:
    """
    Checks if the filesystem is case-sensitive using a temporary file.

    :return: whether the filesystem is case-sensitive.
    """
    with tempfile.NamedTemporaryFile(prefix="TmP") as tmp_file:
        return not os.path.exists(tmp_file.name.lower())


def truncate_text(text: str, max_length: int = 10) -> str:
    """Truncate text to a maximum length.

    :param text (str): Text to truncate.
    :param max_length (int): Maximum length, default is 10 characters.
    :return (str): Truncated text.
    """
    text_width = wcswidth(text)
    if text_width <= max_length:
        return text

    current_width = 0
    truncated_text = ""

    for char in text:
        char_width = wcswidth(char)
        if current_width + char_width > max_length - 3:
            break

        truncated_text += char
        current_width += char_width

    truncated_text += "..."
    space_padding = max_length - wcswidth(truncated_text)
    truncated_text += " " * space_padding
    return truncated_text


def get_timezone() -> pytz.timezone:
    """
    Get the timezone from the user.

    :return: The selected timezone.
    """
    timezone = inquirer.fuzzy(
        message="Select a timezone:",
        choices=pytz.all_timezones,
        match_exact=True,
        default="UTC",
        exact_symbol="",
        max_height=consts.INQUIRER_CHOICES_MAX_VISIBLE_ENTRIES,
        border=True,
    ).execute()
    return pytz.timezone(timezone)


def timedelta_to_str(delta: timedelta) -> str:
    """
    Convert a timedelta object to an approximate time string
    representation rounded to the nearest unit.

    :param delta: The timedelta object.
    :return: The string representation of the timedelta.
    """
    days = delta.days
    hours, remainder = divmod(delta.seconds + 30, 3600)  # Round to nearest hour
    minutes, seconds = divmod(remainder, 60)  # Round to nearest minute

    if days:
        rounded_days = days + (1 if hours >= 12 else 0)
        return f"{rounded_days} day{'s' if rounded_days != 1 else ''}"

    if hours:
        rounded_hours = hours + (1 if minutes >= 30 else 0)
        return f"{rounded_hours} hour{'s' if rounded_hours != 1 else ''}"

    if minutes:
        rounded_minutes = minutes + (1 if seconds >= 30 else 0)
        return f"{rounded_minutes} minute{'s' if rounded_minutes != 1 else ''}"

    return f"{seconds} second{'s' if seconds != 1 else ''}"


def pretty_print_datetime(
    datetime_obj: datetime, timezone: pytz.timezone = pytz.utc
) -> str:
    """
    Pretty print the datetime object into a human-readable string.

    :param datetime_obj: The datetime object.
    :param timezone: The timezone to use.
    :return: The pretty printed datetime string.
    """
    timezone_offset = datetime_obj.utcoffset() // timedelta(hours=1)
    return (
        datetime_obj.strftime(
            f"%B %d, %Y %I:%M %p UTC{'+' if timezone_offset >= 0 else ''}"
            f"{timezone_offset} ({str(datetime_obj.tzinfo)})"
        )
        if timezone != pytz.utc
        else datetime_obj.strftime("%B %d, %Y %I:%M %p %Z")
    )


def utc_timestamp_ms_to_iso8601(timestamp_ms: int) -> str:
    """
    Convert a UTC timestamp in milliseconds to an ISO 8601 formatted string.

    :param timestamp_ms: The timestamp in milliseconds.
    :return: The ISO 8601 formatted string.
    """
    return (
        datetime.fromtimestamp(timestamp=float(timestamp_ms / 1000), tz=pytz.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def generate_webhook_secret() -> str:
    """
    Generate a webhook secret from a secure random source.

    :return: The generated webhook secret.
    """
    secret_contents = secrets.token_bytes(32)
    encoded_contents = base64.b64encode(secret_contents)
    return encoded_contents.decode("utf-8")
