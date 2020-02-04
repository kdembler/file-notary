from hashlib import sha256
from werkzeug.utils import secure_filename
import os
import tempfile


def get_file_hash(file):
    file_bytes = file.read()
    file.seek(0)
    digester = sha256()
    digester.update(file_bytes)
    return '0x' + digester.hexdigest()


def random_hash():
    digester = sha256()
    digester.update(os.urandom(6))
    return '0x' + digester.hexdigest()


def bad_request(message):
    return {'error': message}, 400


def save_temp_file(file):
    filename = secure_filename(file.filename)
    path = os.path.join(tempfile.gettempdir(), filename)
    file.save(path)
    return filename, path
