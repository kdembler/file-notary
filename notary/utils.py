from hashlib import sha256
from werkzeug.utils import secure_filename
import os
import tempfile

def bad_request(message):
    return {'error': message}, 400

def safe_getenv(key):
  value = os.getenv(key)

  if value is None:
    raise Exception(f'{key} variable not found in the env')

  return value
