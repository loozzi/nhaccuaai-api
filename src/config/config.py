from .devConfig import DevConfig
from .productionConfig import ProductionConfig


class Config:
    def __init__(self):
        self.PREFIX_URL = "/api"

    def getDevConfig(self):
        return DevConfig()

    def getProdConfig(self):
        return ProductionConfig()
