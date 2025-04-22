from .envConfig import EnvironmentConfig


class ProductionConfig:
    def __init__(self) -> None:
        self.DEBUG = False
        self.ENV = EnvironmentConfig("prod")
        self.HOST = "0.0.0.0"
        self.PORT = 80
