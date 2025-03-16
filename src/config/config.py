from .devConfig import DevConfig
from .productionConfig import ProductionConfig


class Config:
    def __init__(self):
        self.__devConfig = DevConfig()
        self.__prodConfig = ProductionConfig()

        self.PREFIX_URL = "/api"

    def getDevConfig(self):
        return self.__devConfig

    def getProdConfig(self):
        return self.__prodConfig
