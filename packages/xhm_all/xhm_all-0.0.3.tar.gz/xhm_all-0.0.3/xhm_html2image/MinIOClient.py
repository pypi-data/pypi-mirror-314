import hashlib
import os
from datetime import timedelta

import minio
import mimetypes


class MinIOClient:
    """自建minio oss https://min.io/docs/minio/linux/index.html?ref=con"""

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.minio_conf = self.get_minio_conf()

    def get_minio_conf(self):
        return {
            # 'endpoint': '10.1.251.87:9000',
            # 'secure': False,
            'endpoint': 'fs-oss.fscut.com',
            'secure': True,
            'access_key': 'xrAKwPcaKlmb3UPp8BXL',
            'secret_key': 'OFLjarU1m18XUOJYUlWcGyUSuZEIFOUA5GIUMYpO',
        }

    def auto_object_name(self, file_path: str, object_dir: str = ""):
        # 获取文件名和后缀
        file_dir = os.path.dirname(file_path)
        if not object_dir:
            object_dir = hashlib.md5(file_dir.encode('utf-8')).hexdigest()
        file_name = os.path.basename(file_path)  # 获得文件名，包括后缀
        # file_extension = os.path.splitext(file_name)[1]  # 获得文件后缀
        return f"{object_dir}/{file_name}" if object_dir else file_name

    def upload(self, file_path: str, object_name: str = None,
               content_type=None):

        object_name = object_name if object_name else self.auto_object_name(file_path=file_path)

        content_type = content_type if content_type else mimetypes.guess_type(file_path)[0]
        client = minio.Minio(**self.minio_conf)
        client.fput_object(bucket_name=self.bucket_name, object_name=object_name,
                           file_path=file_path,
                           content_type=content_type
                           )
        return object_name

    def get_presigned_url(self, object_name: str, expires: int = 604800):
        """获取预签名url"""
        client = minio.Minio(**self.minio_conf)
        expires = timedelta(seconds=expires)
        return client.presigned_get_object(bucket_name=self.bucket_name, object_name=object_name, expires=expires)

    def get_url(self, object_name: str):
        """需要自定义访问策略，用gpt写了一个
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::wechat/*"
                    ]
                }
            ]
        }"""
        scheme = "https" if self.minio_conf["secure"] else "http"
        return f"{scheme}://{self.minio_conf['endpoint']}/{self.bucket_name}/{object_name}"

    def load(self):
        client = minio.Minio(**self.minio_conf)
        if not client.bucket_exists(self.bucket_name):
            return None
        data = client.get_object(self.bucket_name, 'wechat2')
        path = "receive.zip"
        with open(path, 'wb') as file_data:
            for d in data.stream(32 * 1024):
                file_data.write(d)
        return data.data


xhm_oss = MinIOClient(bucket_name="wechat")
