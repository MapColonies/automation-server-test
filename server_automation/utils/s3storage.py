# pylint: disable=line-too-long,invalid-name
"""This module provide usefull class that wrapping S3 and provide basic functionality [read and write] with S3 objects"""
import os
import logging
import boto3
import botocore
from server_automation.configuration import config

_log = logging.getLogger('server_automation.utils.s3storage')


class S3Client:
    """
    This class implements s3 functionality
    """
    # pylint: disable=fixme
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key):
        if 'minio' in endpoint_url:  # todo - refactor as validation check
            endpoint_url = endpoint_url.split('minio')[0]
        self._endpoint_url = endpoint_url
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._download_urls = {}

        try:
            self._resource = boto3.resource('s3', endpoint_url=self._endpoint_url,
                                            aws_access_key_id=self._aws_access_key_id,
                                            aws_secret_access_key=self._aws_secret_access_key)
        except Exception as e:
            _log.error('Failed on sign into s3 with error %s', str(e))
            raise e

        try:
            self._client = boto3.client('s3', endpoint_url=self._endpoint_url,
                                        aws_access_key_id=self._aws_access_key_id,
                                        aws_secret_access_key=self._aws_secret_access_key)

        except Exception as e:
            _log.error('Failed on sign into s3 with error %s', str(e))
            raise e

        _log.info('New s3 client object was created with end point: %s', self._endpoint_url)

    def get_client(self):
        """return initialized s3 client object"""
        return self._client

    def create_new_bucket(self, bucket_name):
        """
        This method add new bucket according to provided name
        """
        if not self._resource.Bucket(bucket_name) in self._resource.buckets.all():
            self._resource.create_bucket(Bucket=bucket_name)
            _log.info('New bucket created with name: %s', bucket_name)

        else:
            _log.error('Bucket with name: [%s] already exist on s3, failed on creation', bucket_name)
            raise FileExistsError('Bucket with name: [%s] already exist on s3, failed on creation' % bucket_name)

    def delete_bucket(self, bucket_name):
        """
        This method empty given bucket and delete bucket
        """
        if not self._resource.Bucket(bucket_name) in self._resource.buckets.all():
            raise FileNotFoundError('Bucket with name: [%s] not exist on s3, failed on deletion' % bucket_name)

        self._resource.Bucket(bucket_name).objects.all().delete()
        self._resource.Bucket(bucket_name).delete()

    def empty_bucket(self, bucket_name):
        """
        This method empty the given bucket without deletion of bucket
        """
        if not self._resource.Bucket(bucket_name) in self._resource.buckets.all():
            raise FileNotFoundError('Bucket with name: [%s] not exist on s3, failed on deletion' % bucket_name)

        self._resource.Bucket(bucket_name).objects.all().delete()

    def upload_to_s3(self, full_path, bucket, object_key):
        """
        basic file uploading to s3
        :param full_path: file system location of file to upload
        :param bucket: bucket name to destination uploading
        :param object_key: name of file to uploading into s3
        """
        if not os.path.exists(full_path):
            raise FileExistsError('File not exist on given directory: %s' % full_path)

        try:
            # self._client.upload_file(full_path, bucket, object_key)
            self._resource.Bucket(bucket).upload_file(full_path, object_key)
            _log.info('Success on uploading %s into s3', os.path.basename(full_path))
        except Exception as e:
            _log.error('Failed uploading file [%s] into s3 with error: %s', object_key, str(e))
            raise Exception('Failed uploading file [%s] into s3 with error: %s' % (full_path, str(e)))  # pylint: disable=raise-missing-from

    def download_from_s3(self, bucket, object_key, destination):
        """
        This method download object into local file system. as default on "/tmp/"
        """
        self._resource.Bucket(bucket).download_file(object_key, destination)
        _log.debug('File was saved on: %s', str(destination))

    def create_download_url(self, bucket, object_key):
        """
        Generate new download url from S3 according to specific bucket and object_key.
        Add new key (object_key) into download_urls dictionary
        """
        self._download_urls[":".join([bucket, object_key])] = self._client.generate_presigned_url('get_object',
                                                                                                  Params={'Bucket': bucket,
                                                                                                          'Key': object_key},
                                                                                                  ExpiresIn=config.S3_DOWNLOAD_EXPIRATION_TIME)

    def is_file_exist(self, bucket_name, object_key):
        """
        Validate if some file exists on specific bucket in OS based on provided object key and bucket name
        """
        if not self._resource.Bucket(bucket_name) in self._resource.buckets.all():
            _log.debug('Bucket with name: [%s] not exist on s3', bucket_name)
            return False

        try:
            self._resource.Object(bucket_name, object_key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False

            _log.error(str(e))
            raise e
        except Exception as e2:
            _log.error(str(e2))
            raise e2

        return True
        # def get_download_urls(self):
        # return self._download_urls
