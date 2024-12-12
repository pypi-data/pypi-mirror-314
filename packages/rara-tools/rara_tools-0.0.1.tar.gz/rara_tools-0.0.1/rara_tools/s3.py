import os
import uuid
from typing import Optional
from minio import Minio

from .exceptions import S3InitException, S3ConnectionException, S3InputException


class S3Files:
    """ A class to manage file uploads and downloads from/to S3.
    """

    def __init__(
            self,
            url: Optional[str] = None,
            access_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            bucket: Optional[str] = None
        ):
        if not url:
            raise S3InitException("S3 URL not set!")
        if not access_key:
            raise S3InitException("S3 access key not set!")
        if not secret_key:
            raise S3InitException("S3 secret key not set!")
        if not bucket:
            raise S3InitException("Bucket not set!")      
        self.bucket = bucket
        self.minio_client = Minio(
            url,
            access_key=access_key,
            secret_key=secret_key
        )
        # Check S3 connection
        try:
            self.minio_client.bucket_exists(bucket)
        except Exception as e:
            raise S3ConnectionException(f"Error connecting to bucket: {e}")

    def _put_file(self, file_path: str, s3_path_name: str):
        if not os.path.exists(file_path):
            raise S3InputException(f"File '{file_path}' does not exist in file system!")
        return self.minio_client.fput_object(self.bucket, s3_path_name, file_path)

    def list(self, prefix: Optional[str] = ""):
        """Lists all available files in S3 bucket.
        :param: prefix str: Limits the listing to a given prefix.
        :return: List of file paths in S3.
        """
        list_of_objects = self.minio_client.list_objects(self.bucket, prefix=prefix, recursive=True)
        list_of_objects = [o.object_name for o in list_of_objects]
        return list_of_objects

    def delete(self, path: str):
        """Deletes file in S3.
        :param: path str: Path of the file in S3 to be deleted.
        """
        list_of_objects = self.minio_client.list_objects(self.bucket, prefix=path, recursive=True)
        list_of_objects = [o.object_name for o in list_of_objects]
        for path_to_delete in list_of_objects:
            self.minio_client.remove_object(self.bucket, path_to_delete)

    def download(self, path: str, download_dir: Optional[str] = "."):
        """Downloads file or folder from S3.
        :param: path str: Path to the file or folder in S3.
        :param: download_dir str: Directory to download the files and folders into.
        :return: Generate listing of local paths of the downloaded files. 
        """
        list_of_objects = list(self.minio_client.list_objects(self.bucket, prefix=path, recursive=True))
        for minio_object in list_of_objects:
            full_path = os.path.join(download_dir, minio_object.object_name)
            self.minio_client.fget_object(self.bucket, minio_object.object_name, full_path)
            yield full_path

    def upload(self, path: str, prefix: Optional[str] = ""):
        """Uploads file or folder to S3 bucket.
        :param: path str: Path to the file to upload in local file system.
        :param: prefix str: Optional prefix for S3 path.
        :returns: File path of the uploaded file or folder in S3.
        """
        path_name = os.path.split(path)[-1]
        # Manage directories
        if os.path.isdir(path):
            s3_path_prefix = f"{prefix}{uuid.uuid4().hex}"
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    extension = file.split(".")[-1]
                    s3_file_name = f"{uuid.uuid4().hex}.{extension}"
                    s3_path_name = os.path.join(s3_path_prefix, s3_file_name)
                    self._put_file(file_path, s3_path_name)
            return s3_path_prefix
        # Manage single files
        else:
            extension = path_name.split(".")[-1]
            s3_path_name = f"{prefix}{uuid.uuid4().hex}.{extension}"
            self._put_file(path, s3_path_name)
            return s3_path_name
