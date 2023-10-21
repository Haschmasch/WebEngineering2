"""
Provides hashing functionalities for hashing passwords.
"""


import hashlib
import secrets


def generate_salt():
    """
    Generates a cryptographically strong pseudo-random salt.
    :return: The salt as string.
    """
    return secrets.token_hex(16)


def generate_hash(value, salt):
    """
    Generates a hash value for the specified value using a salt.
    :param value: The value to be hashed.
    :param salt: The salt for the value.
    :return: The salted hash.
    """
    h = hashlib.sha256()
    h.update(str.encode(salt))
    h.update(str.encode(value))
    return h.hexdigest()

