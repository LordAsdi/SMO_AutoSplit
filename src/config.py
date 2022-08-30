import logging
import shutil
import json
import os


class Config:
    appdata = os.path.join(os.path.expandvars(r'%LOCALAPPDATA%'), "Lord Asdi", "SMO AutoSplit")
    version_path = ".version"
    config_path = os.path.join(appdata, "config.json")
    default_path = "defaults.json"

    version = ""
    config = None
    default = None

    @staticmethod
    def init():
        Config.load_version()
        Config.load_config()
        Config.load_default()

    @staticmethod
    def load_config():
        if not os.path.isfile(Config.config_path):
            shutil.copy(Config.default_path, Config.config_path)
        try:
            with open(Config.config_path, "r") as file:
                Config.config = json.load(file)
            return True
        except Exception as e:
            Config.config = None
            logging.exception(e)
            return False

    @staticmethod
    def save_config():
        try:
            with open(Config.config_path + "tmp", "w") as file:
                json.dump(Config.config, file, indent=4)
                file.flush()
                os.fsync(file)
            os.replace(Config.config_path + "tmp", Config.config_path)
            return True
        except Exception as e:
            logging.exception(e)
            os.remove(Config.config_path + "tmp")
            return False

    @staticmethod
    def load_default():
        try:
            with open(Config.default_path, "r") as file:
                Config.default = json.load(file)
            return True
        except Exception as e:
            Config.default = None
            logging.exception(e)
            return False

    @staticmethod
    def load_version():
        try:
            with open(Config.version_path, "r") as file:
                version = file.readline()
            Config.version = version
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def get_key(key):
        if not key:
            return None

        if not Config.config:
            config_loaded = Config.load_config()
        else:
            config_loaded = True

        if not Config.default:
            config_loaded = config_loaded or Config.load_default()
        else:
            config_loaded = True

        if not config_loaded:
            logging.warning(f"No config file available")
            return None

        try:
            if Config.config and key in Config.config:
                return Config.config[key]
            elif Config.default and key in Config.default:
                return Config.default[key]
            else:
                logging.warning(f"Key \"{key}\" not found in \"{Config.config_path}\" or \"{Config.default_path}\"")
                return None
        except Exception as e:
            logging.exception(e)
            return None

    @staticmethod
    def set_key(key, value):
        if not key:
            return

        if not Config.config:
            if not Config.load_config():
                logging.warning(f"Config file not available")
                return

        try:
            Config.config[key] = value
        except Exception as e:
            logging.exception(e)
            return

        Config.save_config()
