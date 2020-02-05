import os
import random
import string


def bad_request(message):
    return {'msg': message}, 400


def safe_getenv(key):
    value = os.getenv(key)

    if value is None:
        raise Exception(f'{key} variable not found in the env')

    return value


def generate_random_code():
    generator = random.SystemRandom()
    random_digits = (generator.choice(string.digits) for _ in range(6))
    return ''.join(random_digits)
