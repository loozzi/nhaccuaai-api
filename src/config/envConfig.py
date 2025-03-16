import os

from dotenv import load_dotenv


class EnvironmentConfig:
    def __init__(self, env_name: str) -> None:
        load_dotenv(env_name + ".env")
        self.ENV_NAME = env_name
        self.SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
