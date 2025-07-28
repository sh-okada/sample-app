import os


class DB:
    USER: str = os.getenv("DB_USER", "postgres")
    PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", 5432))
    NAME: str = os.getenv("DB_NAME", "postgres")


class JWT:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 30))
