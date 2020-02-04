import boto3
import os
import multiprocessing as mp
import logging
from botocore.exceptions import NoCredentialsError
from utils import safe_getenv


def start_uploader():
    upload_queue = mp.Queue()
    uploader = Uploader(upload_queue)
    uploader.run()

    return uploader, upload_queue

class Uploader:
    def __init__(self, upload_queue):
        self.upload_queue = upload_queue
        self.logger = logging.getLogger('uploader')

        self._set_s3_client()
        self.bucket_name = safe_getenv('S3_BUCKET_NAME')

        self.logger.info(f'initialized for bucket {self.bucket_name}')

    def generate_download_url(self, file_name):
        url = self.s3.generate_presigned_url('get_object',
                                             Params={'Bucket': self.bucket_name,
                                                     'Key': file_name},
                                             ExpiresIn=60)
        return url

    def run(self):
        p = mp.Process(target=self._process_queue)
        p.start()

    def _set_s3_client(self):
        access_key = safe_getenv('S3_ACCESS_KEY')
        secret_key = safe_getenv('S3_SECRET_KEY')

        self.s3 = boto3.client('s3', aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               region_name='eu-central-1',
                               config=boto3.session.Config(signature_version='s3v4'))

    def _process_queue(self):
        self.logger.info('starting queue processing')
        while True:
            self.logger.info('waiting for file to process')

            try:
                filename, file_stream = self.upload_queue.get()
            except KeyboardInterrupt:
                self.logger.info('exitting')
                break

            self.logger.info(f'processing {filename}')
            try:
                self.s3.upload_fileobj(file_stream, self.bucket_name, filename)
                self.logger.info(f'processed {filename}')
            except NoCredentialsError:
                self.logger.error(f'invalid credentials')
