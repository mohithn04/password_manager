from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os
import base64

def load_or_create_salt():
    if not os.path.exists('salt.bin'):
        salt = os.urandom(16)
        with open('salt.bin', 'wb') as f:
            f.write(salt)
    else:
        with open('salt.bin', 'rb') as f:
            salt = f.read()
    return salt

def get_key_from_password(password, salt):
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,  # this is a random value to make password cracking harder
                # we should store it securely and reuse it each time we derive the key
    iterations=600_000,
    backend=default_backend()
  )
  return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_password(key, password):
  fernet = Fernet(key)
  return fernet.encrypt(password.encode())

def decrypt_password(key, encrypted_password):
  fernet = Fernet(key)
  return fernet.decrypt(encrypted_password).decode()
