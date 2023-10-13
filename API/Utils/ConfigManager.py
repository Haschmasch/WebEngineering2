import os
from API.Utils.FileOperations import read_json


class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config_data = read_json(self.config_path)

    @property
    def chat_root_dir(self):
        return os.path.abspath(self.config_data["ChatRootDir"])

    @property
    def offer_root_dir(self):
        return os.path.abspath(self.config_data["OfferRootDir"])

    @property
    def db_url(self):
        return self.config_data['ConnectionString']

