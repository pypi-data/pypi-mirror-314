import hashlib


# Hash Function for key
def hash_this(string):
    return hashlib.sha256(str(string).encode('utf-8')).hexdigest()
