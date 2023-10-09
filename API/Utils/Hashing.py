import hashlib
import secrets


def generate_salt():
    return secrets.token_hex(16)


def generate_hash(value, salt):
    h = hashlib.sha256()
    h.update(str.encode(salt))
    h.update(str.encode(value))
    return h.hexdigest()

