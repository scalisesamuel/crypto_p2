import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
language = "Python"
security_suite = "cryptography"
task = "task 1"

print("\nLanguage:\t", language, "\nCryptographic Library:\t", security_suite, "\nTask:\t", task)
print("Resources:\tClass Notes and Cryptography.io")

print("\nRandom Number Test")
rbytes1 = os.urandom(128)
rbytes2 = os.urandom(256)
print(rbytes1)
print(rbytes2)

print("\nAES Test")
backend = default_backend()
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
pt = b'Hello This is the secret message'
print("Plain Text:\t", pt)
ct = encryptor.update(pt) + encryptor.finalize()
decryptor = cipher.decryptor()
ptNew = decryptor.update(ct) + decryptor.finalize()
print("Cipher Text:\t", ct)
print("Decrypted Plain Text:\t", ptNew)

print("\nSHA 256 Test")
print("input 1:\t", b'abc')
print("input 1 size:\t", b'abc'.__sizeof__())
print("input 2:\t", b'123')
print("input 2 size:\t", b'123'.__sizeof__())
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(b'abc')
digest.update(b'123')
digest.finalize()
print("size of digest:\t", digest.__sizeof__())
