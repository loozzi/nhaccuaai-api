from .devConfig import DevConfig
from .productionConfig import ProductionConfig


class Config:
    def __init__(self):
        self.__devConfig = DevConfig()
        self.__prodConfig = ProductionConfig()

    def getDevConfig(self):
        return self.__devConfig

    def getProdConfig(self):
        return self.__prodConfig
