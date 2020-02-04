from hashlib import sha256
from werkzeug.utils import secure_filename
import os
import tempfile

def bad_request(message):
    return {'error': message}, 400
