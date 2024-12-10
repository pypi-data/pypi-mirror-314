import json
from Crypto.Cipher import AES
from django.conf import settings


def encrypt(obj):
    cipher = AES.new(key_as_bytes(), AES.MODE_EAX)

    # Encrypt
    ciphertext, tag = cipher.encrypt_and_digest(str.encode(json.dumps(obj)))
    encrypted = [x for x in (cipher.nonce, tag, ciphertext)]
    return b''.join(encrypted)


def decrypt(obj):
    nonce, tag, ciphertext = obj[:16], obj[16:32], obj[32:]
    try:
        cipher = AES.new(key_as_bytes(), AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(data)
    except ValueError:
        return None


def key_as_bytes():
    bytes = settings.SECRET_KEY.encode('utf-8')[0:32]
    # If the key is less than 32 bytes, pad it
    while len(bytes) < 32:
        bytes += bytes
    return bytes[0:32]
