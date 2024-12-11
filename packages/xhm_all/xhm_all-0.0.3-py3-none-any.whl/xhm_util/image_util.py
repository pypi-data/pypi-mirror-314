import requests
from urllib.parse import urlparse
from enum import Enum


class FileType(Enum):
    IMAGE = "Image"
    PDF = "PDF"
    VIDEO = "Video"
    AUDIO = "Audio"
    TEXT = "Text"
    ZIP_ARCHIVE = "ZIP Archive"
    WORD_DOCUMENT = "Word Document"
    EXCEL_DOCUMENT = "Excel Document"
    POWERPOINT_DOCUMENT = "PowerPoint Document"
    JSON_DOCUMENT = "JSON Document"
    APPLICATION_FILE = "Application File"
    UNKNOWN = "Unknown File Type"
    INVALID_URL = "Invalid URL"
    REQUEST_FAILED = "Request Failed"


def _is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False


def get_url_file_type(url):
    if not _is_valid_url(url):
        return FileType.INVALID_URL
    try:
        # 发送 HEAD 请求获取响应头
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')

        # 检查不同的 MIME 类型
        if content_type.startswith('image/'):
            return FileType.IMAGE
        elif content_type == 'application/pdf':
            return FileType.PDF
        elif content_type.startswith('video/'):
            return FileType.VIDEO
        elif content_type.startswith('audio/'):
            return FileType.AUDIO
        elif content_type.startswith('text/'):
            return FileType.TEXT
        elif content_type in ['application/zip', 'application/x-zip-compressed']:
            return FileType.ZIP_ARCHIVE
        elif content_type in ['application/msword',
                              'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return FileType.WORD_DOCUMENT
        elif content_type in ['application/vnd.ms-excel',
                              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return FileType.EXCEL_DOCUMENT
        elif content_type == 'application/vnd.ms-powerpoint':
            return FileType.POWERPOINT_DOCUMENT
        elif content_type.startswith('application/json'):
            return FileType.JSON_DOCUMENT
        elif content_type.startswith('application/'):
            return FileType.APPLICATION_FILE
        else:
            return FileType.UNKNOWN

    except requests.RequestException:
        return FileType.REQUEST_FAILED


def is_url_of_type(url, file_type):
    if not isinstance(file_type, FileType):
        raise ValueError("file_type must be an instance of FileType Enum.")

    detected_file_type = get_url_file_type(url)
    return detected_file_type == file_type
