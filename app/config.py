<<<<<<< HEAD
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = '.env'


settings = Settings()
=======
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = '.env'

settings = Settings()
>>>>>>> 28fbc88f2d44fd64d2eeaa3f5bef0db91ad3df05
