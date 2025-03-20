import os

from dotenv import load_dotenv


class EnvironmentConfig:
    def __init__(self, env_name: str) -> None:
        load_dotenv(env_name + ".env")
        self.ENV_NAME = env_name
        self.SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
        self.JWT_SECRET = os.getenv("JWT_SECRET")
        self.JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS"))
        self.JWT_REFRESH_EXP_DAYS = int(os.getenv("JWT_REFRESH_EXP_DAYS"))
