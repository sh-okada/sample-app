from pydantic_settings import BaseSettings


class DB(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"


class JWT(BaseSettings):
    jwt_secret_key: str = "fake_secret_key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
