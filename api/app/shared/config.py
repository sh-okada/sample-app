from pydantic_settings import BaseSettings


class DB(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


class JWT(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    refresh_jwt_secret_key: str
    refresh_jwt_algorithm: str
    refresh_jwt_expire_days: int
