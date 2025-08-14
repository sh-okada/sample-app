from pydantic_settings import BaseSettings


class DB(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"


class JWT(BaseSettings):
    JWT_SECRET_KEY: str = "fake_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
