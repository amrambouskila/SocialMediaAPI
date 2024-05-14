<<<<<<< HEAD
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
=======
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
>>>>>>> 28fbc88f2d44fd64d2eeaa3f5bef0db91ad3df05
    return pwd_context.verify(plain_password, hashed_password)