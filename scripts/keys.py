from os import urandom
from base64 import b64encode

print(f"Encryption key:\t\t {b64encode(urandom(16)).decode('utf-8')}")
print(f"Sign key:\t\t {b64encode(urandom(16)).decode('utf-8')}")
