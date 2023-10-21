"""
Helper file for reading the config.json.
Properties can be accessed via the attributes of the ConfigManager class.
"""

from API.Utils.FileOperations import read_json


"""ConfigManager is used to read the configuration file"""""


class ConfigManager:
    def __init__(self, path="Utils/config.json"):
        self.path = path
        self.config_data = read_json(self.path)

    @property
    def chat_root_dir(self):
        return self.config_data["ChatRootDir"]

    @property
    def offer_root_dir(self):
        return self.config_data["OfferRootDir"]

    @property
    def db_url(self):
        return self.config_data["ConnectionString"]

    @property
    def jwt_secret(self):
        return self.config_data["JwtSecret"]


configuration = ConfigManager()
