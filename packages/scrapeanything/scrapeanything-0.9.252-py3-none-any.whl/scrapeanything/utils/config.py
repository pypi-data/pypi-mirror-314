from configparser import ConfigParser
import re

class Config:

    def __init__(self, path: str):
        self.config = ConfigParser()
        # read config.ini file
        self.config.read(path)

    def set(self, section: str, key: str, value: str) -> None:
        if section in self.config and key in self.config[section]:
            self.config[section][key] = value

    def get(self, section: str, key: str, default: any=None):
        # get config value
        if section in self.config and key in self.config[section]:
            response = self.config[section][key]

            if response == 'True': return True
            elif response == 'False': return False
            elif bool(re.search('^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$', response)) is True and '.' in response: return float(response)
            elif bool(re.search('^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$', response)) is True and '.' not in response: return int(response)
            else: return response

        elif (section in self.config and key not in self.config[section]) or (section not in self.config):
            if default is not None: return default
            else: return None
        else: raise Exception('Configuration not found!')