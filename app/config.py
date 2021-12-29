from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_port: str
    database_name: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 360
    class Config:
        env_file = '../.env'

settings = Settings()

# database_hostname: str = "localhost"
# database_username: str = "postgres"
# database_port: str = "5432"
# database_name: str = "fastapi"
# database_password: str = "Paul1996!"
# secret_key: str = "nonwononxonwponcp"
# algorithm: str = "HS256"
# access_token_expire_minutes: int = 360
# class Config:
#     env_file = '.env'
