import datetime
import logging
import pathlib
from io import BytesIO
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_pymongo import PyMongo
from pymongo.errors import ServerSelectionTimeoutError

import utils
from logger import logger_init
from uploader import start_uploader
from eth import start_notary

# initial configuration
dotenv_file_path = pathlib.Path(__file__).parent.absolute().parent / '.env'
load_dotenv(dotenv_path=dotenv_file_path)
logger_init()

logger = logging.getLogger()

# configure flask
app = Flask(__name__)
CORS(app)

mongo_host = utils.safe_getenv('MONGO_HOST')
mongo_uri = f'mongodb://{mongo_host}/notary'
app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app, serverSelectionTimeoutMS = 2000)
try:
    # check connection
    mongo.cx.server_info()
except ServerSelectionTimeoutError:
    raise Exception(f'failed to connect to db at {mongo_uri}')
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
        return utils.bad_request_response('Body must be JSON')

    user_code = request.json['user_code']
    if not user_code:
        return utils.bad_request_response('Missing user_code param')

    user = mongo.db.users.find_one({'_id': user_code})
    if not user:
        return utils.unauthorized_response('Unknown user code')

    access_token = create_access_token(identity=user_code)

    return {'access_token': access_token}


@app.route('/files', methods=['GET'])
@jwt_required
def get_files():
    user_code = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': user_code})
    user_files = user['files']
    mapped_files = [utils.sanitize_file_dict(file) for file in user_files]
    return jsonify(mapped_files), 200


@app.route('/files', methods=['POST'])
@jwt_required
def upload_file():
    if 'file' not in request.files:
        return utils.bad_request_response('No file in request')

    file = request.files['file']
    filename = file.filename

    if not filename:
        return utils.bad_request_response('Filename cannot be empty')

    file_bytes = file.read()
    file.close()
    file_stream = BytesIO(file_bytes)

    file_id = str(uuid4())
    user_code = get_jwt_identity()
    new_file = {
        '_id': file_id,
        'created': datetime.datetime.utcnow(),
        'name': filename,
    }
    mongo.db.users.update({'_id': user_code}, {'$push': {'files': new_file}})
    logger.info(f'saved file with id {file_id}')

    upload_queue.put((file_id, file_stream))
    notary_queue.put((file_id, file_bytes))

    return utils.sanitize_file_dict(new_file), 200


@app.route('/files/<file_id>')
@jwt_required
def generate_download_url(file_id):
    if not file_id:
        return utils.bad_request_response('Missing file id')

    user_code = get_jwt_identity()
    result = mongo.db.users.find_one({'_id': user_code, 'files._id': file_id}, {'files.$': 1})
    if not result:
        return {'msg': 'File not found'}, 404
    raw_file = result['files'][0]

    file = utils.sanitize_file_dict(raw_file)
    url = uploader.generate_download_url(file_id)
    file['download_url'] = url
    return file, 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
