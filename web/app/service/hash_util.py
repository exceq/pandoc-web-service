import hashlib


def generate_hash(text: str):
    return hashlib.md5(bytes(text, 'utf-8')).hexdigest()
