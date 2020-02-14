import os
import random
import string


def bad_request_response(msg):
    return create_response(msg, 400)


def unauthorized_response(msg):
    return create_response(msg, 401)


def create_response(msg, code=200):
    return {'msg': msg}, code


def safe_getenv(key):
    value = os.getenv(key)

    if value is None:
        raise Exception(f'{key} variable not found in the env')

    return value


def generate_random_code():
    generator = random.SystemRandom()
    random_digits = (generator.choice(string.digits) for _ in range(6))
    return ''.join(random_digits)


def sanitize_file_dict(file):
    return {'id': file['_id'], 'created': file['created'].isoformat(), 'filename': file['filename']}
