# pylint: disable-all
""" Test file not for deploy """
import os
from server_automation.utils import s3storage

MINIO_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
MINIO_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
endpoint_url = 'http://localhost:9000/minio/'
BUCKET = 'test2'
full_path = '/home/ronenk1/dev/automation-server-test/samples/request_sanity.json'

sreader = s3storage.S3Client(endpoint_url, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
# print(sreader.get_download_urls())
sreader.upload_to_s3(full_path, BUCKET, os.path.basename(full_path))
sreader.create_download_url(BUCKET, os.path.basename(full_path))
sreader.download_from_s3(BUCKET, os.path.basename(full_path))
print(sreader.get_download_urls())
sreader.get_download_urls()['test2:request_sanity.json']
print('developing')
