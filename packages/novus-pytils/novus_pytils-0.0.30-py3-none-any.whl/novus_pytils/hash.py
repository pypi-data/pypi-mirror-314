import hashlib
def get_file_md5_hash(file_path):
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5(file.read()).hexdigest()
    return md5_hash

def get_str_md5_hash(string):
    return hashlib.md5(string.encode()).hexdigest()

def get_str_sha256_hash(string):
    return hashlib.sha256(string.encode()).hexdigest()

def get_file_sha256_hash(file_path):
    with open(file_path, 'rb') as file:
        sha256_hash = hashlib.sha256(file.read()).hexdigest()
    return sha256_hash

