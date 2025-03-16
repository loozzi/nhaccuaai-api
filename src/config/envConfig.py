import os

from dotenv import load_dotenv


class EnvironmentConfig:
    def __init__(self, env_name: str) -> None:
        load_dotenv(env_name + ".env")
        self.ENV_NAME = env_name
        self.URI_DB = os.getenv("URI_DB")
