import os
import json
from .logger import logger

class Config:
    def __init__(self, path: str):
        try:
            with open(path, "r") as file:
                self.my_config = json.load(file)
                for key, value in self.my_config.items():
                    os.environ[key] = value
        except FileNotFoundError:
            logger.error("No config file found, will rely on environment variables")
