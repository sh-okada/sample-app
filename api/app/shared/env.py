import os


class DB:
    USER: str = os.getenv("DB_USER", "")
    PASSWORD: str = os.getenv("DB_PASSWORD", "")
    HOST: str = os.getenv("DB_HOST", "")
    PORT: str = os.getenv("DB_PORT", "")
    NAME: str = os.getenv("DB_NAME", "")


class JWT:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 30))
