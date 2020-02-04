import boto3
import os
import multiprocessing as mp
import logging
from botocore.exceptions import NoCredentialsError


class Uploader:
    def __init__(self, upload_queue, log_queue):
        access_key = os.getenv('ACCESS_KEY')
        secret_key = os.getenv('SECRET_KEY')
        bucket_name = os.getenv('BUCKET_NAME')

        if access_key is None or secret_key is None:
            raise Exception('AWS Credentials not found')
        if bucket_name is None:
            raise Exception('Bucket name not defined')

        self.s3 = boto3.client('s3', aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               region_name='eu-central-1',
                               config=boto3.session.Config(signature_version='s3v4'))
        self.bucket_name = bucket_name

        self.upload_queue = upload_queue
        self.log_queue = log_queue
        self.logger = logging.getLogger('uploader')
        self.logger.info(f'initialized for bucket {bucket_name}')

    def generate_download_url(self, file_name):
        url = self.s3.generate_presigned_url('get_object',
                                             Params={'Bucket': self.bucket_name,
                                                     'Key': file_name},
                                             ExpiresIn=60)
        return url

    def run(self):
        p = mp.Process(target=self.process_queue)
        p.start()

    def process_queue(self):
        self.logger.info('starting queue processing')
        while True:
            self.logger.info('waiting for file to process')
            filename, filepath = self.upload_queue.get()
            self.logger.info(f'processing {filename}')
            try:
                # TODO: consider using upload_fileobj
                self.s3.upload_file(filepath, self.bucket_name, filename)
                os.remove(filepath)
                self.logger.info(f'processed {filename}')
            except NoCredentialsError:
                self.logger.error(f'invalid credentials')
