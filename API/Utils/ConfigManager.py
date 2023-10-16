from API.Utils.FileOperations import read_json


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
        return self.config_data['ConnectionString']


configuration = ConfigManager()
