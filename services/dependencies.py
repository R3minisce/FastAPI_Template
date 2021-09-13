from bcrypt import gensalt, hashpw


"""
# Class Dependencies
"""
def setattrs(_self, **kwargs):
    for k, v in kwargs.items():
        setattr(_self, k, v)


"""
# Methods Dependencies
"""
def hash_password(password: str, salt: bytes) -> bytes:
    salt = gensalt() if salt is None else salt
    password = hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return password, salt.decode('utf-8')
