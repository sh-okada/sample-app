from pydantic_settings import BaseSettings


class DB(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"


class JWT(BaseSettings):
    jwt_secret_key: str = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
