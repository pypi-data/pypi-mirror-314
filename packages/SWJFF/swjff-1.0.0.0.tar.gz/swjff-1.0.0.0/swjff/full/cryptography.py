from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
import base64, os


def get_key_from_password(password: str, salt: bytes, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def encrypt(data: bytes, password: str):
    salt = os.urandom(16)
    cipher = Fernet(get_key_from_password(password, salt))
    return salt + cipher.encrypt(data)


def decrypt(data: bytes, password: str):
    salt, data = data[:16], data[16:]
    cipher = Fernet(get_key_from_password(password, salt))
    return cipher.decrypt(data)
