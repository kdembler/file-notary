#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from logger import logger_init
from uploader import start_uploader
from eth import start_notary
from io import BytesIO
import utils
import logging
import datetime

# initial configuration
load_dotenv()
logger_init()

logger = logging.getLogger()

# configure flask
app = Flask(__name__)
CORS(app)
mongo_uri = utils.safe_getenv('MONGO_URI')
app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app)
logger.info(f'initiated db connection to {mongo_uri}')

# create workers
uploader, upload_queue = start_uploader()
notary_queue = start_notary()


@app.route('/register', methods=['POST'])
def register():
    user_code = ''

    while not user_code:
        new_code = utils.generate_random_code()
        user_with_code = mongo.db.users.find_one({'_id': new_code})
        if user_with_code is None:
            user_code = new_code

    user = {
        '_id': user_code,
        'created': datetime.datetime.utcnow(),
        'files': []
    }
    mongo.db.users.insert(user)

    return {'user_code': user_code}


@app.route('/upload', methods=['POST'])
def upload():
    logger.info('processing request')
    if 'file' not in request.files:
        return utils.bad_request('No file in request')
    file = request.files['file']
    filename = file.filename
    if filename == '':
        return utils.bad_request('Empty filename')

    file_bytes = file.read()
    file.close()
    file_stream = BytesIO(file_bytes)

    upload_queue.put((filename, file_stream))
    notary_queue.put((filename, file_bytes))

    return {'file_name': filename}, 200


@app.route('/download-url')
def generate_download_url():
    file = request.args.get('file')
    if file is None:
        return utils.bad_request('Missing file query param')
    if len(file) < 1:
        return utils.bad_request('File name too short')
    url = uploader.generate_download_url(file)
    return {'url': url}, 200
