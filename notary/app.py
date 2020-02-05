#!/usr/bin/env python3

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from logger import logger_init
from uploader import start_uploader
from eth import start_notary
from io import BytesIO
from uuid import uuid4
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

jwt_secret = utils.safe_getenv('JWT_SECRET')
app.config['JWT_SECRET_KEY'] = jwt_secret
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
jwt = JWTManager(app)

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
    logger.debug('user created')

    access_token = create_access_token(identity=user_code)
    return {'user_code': user_code, 'access_token': access_token}


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return utils.bad_request('Body must be JSON')

    user_code = request.json['user_code']
    if not user_code:
        return utils.bad_request('Missing user_code param')

    user = mongo.db.users.find_one({'_id': user_code})
    if not user:
        return {'msg': 'Unknown user code'}, 401

    access_token = create_access_token(identity=user_code)

    return {'access_token': access_token}


@app.route('/files', methods=['GET'])
@jwt_required
def get_files():
    user_code = get_jwt_identity()
    user_files = mongo.db.users.find_one({'_id': user_code})['files']
    mapped_files = [utils.sanitize_file_dict(file) for file in user_files]
    return jsonify(mapped_files), 200


@app.route('/files', methods=['POST'])
@jwt_required
def upload_file():
    if 'file' not in request.files:
        return utils.bad_request('No file in request')

    file = request.files['file']
    filename = file.filename

    if not filename:
        return utils.bad_request('Filename cannot be empty')

    file_bytes = file.read()
    file.close()
    file_stream = BytesIO(file_bytes)

    file_id = str(uuid4())
    user_code = get_jwt_identity()
    user_file = {
        '_id': file_id,
        'created': datetime.datetime.utcnow(),
        'filename': filename,
    }
    mongo.db.users.update({'_id': user_code}, {'$push': {'files': user_file}})
    logger.info(f'saved file with id {file_id}')

    upload_queue.put((file_id, file_stream))
    notary_queue.put((file_id, file_bytes))

    return {'id': file_id}, 200


@app.route('/files/<file_id>')
@jwt_required
def generate_download_url(file_id):
    if not file_id:
        return utils.bad_request('Missing file id')

    user_code = get_jwt_identity()
    user_files = mongo.db.users.find_one({'_id': user_code})['files']
    raw_file = next((file for file in user_files if file['_id'] == file_id), None)
    if not raw_file:
        return {'msg': 'File not found'}, 404

    file = utils.sanitize_file_dict(raw_file)
    url = uploader.generate_download_url(file_id)
    file['download_url'] = url
    return file, 200
