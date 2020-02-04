#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from uploader import Uploader
from logger import logger_init
from eth import start_notary
import utils
import logging
import multiprocessing as mp

# initial configuration
load_dotenv()
log_queue, log_listener = logger_init()

logger = logging.getLogger()

# configure flask
app = Flask(__name__)
CORS(app)

# create uploader worker
# TODO: move queue creation to uploader, like notary
upload_queue = mp.Queue()
uploader = Uploader(upload_queue, log_queue)
uploader.run()

notary_queue = start_notary()


@app.route('/upload', methods=['POST'])
def upload():
    logger.info('processing request')
    if 'file' not in request.files:
        return utils.bad_request('No file in request')
    file = request.files['file']
    if file.filename == '':
        return utils.bad_request('Empty filename')

    # TODO: move hashing to notary thread
    file_hash = utils.get_file_hash(file)
    file_name, file_path = utils.save_temp_file(file)

    upload_queue.put((file_name, file_path))
    notary_queue.put((file_name, file_hash))

    return {'file_hash': file_hash, 'file_name': file_name}, 200


@app.route('/download-url')
def generate_download_url():
    file = request.args.get('file')
    if file is None:
        return utils.bad_request('Missing file query param')
    if len(file) < 1:
        return utils.bad_request('File name too short')
    url = uploader.generate_download_url(file)
    return {'url': url}, 200
