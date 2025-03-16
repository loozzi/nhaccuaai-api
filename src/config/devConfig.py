from .envConfig import EnvironmentConfig


class DevConfig:
    def __init__(self):
        self.DEBUG = True
        self.ENV = EnvironmentConfig("dev")
        self.HOST = "0.0.0.0"
        self.PORT = 5000
