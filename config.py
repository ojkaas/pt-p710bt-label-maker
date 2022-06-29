import json
import os

import appdirs

CONFIG_FILE = os.path.join(appdirs.user_config_dir(),'pt-p710bt.json')


def load_config() -> dict:
    try:
        with open(CONFIG_FILE, 'r') as fd:
            config = json.load(fd)
            return config
    except:
        return {}


def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as fd:
        json.dump(config, fd)


def get_default_bt() -> str:
    return load_config().get('default_bt')


def set_default_bt(default_bt: str):
    config = load_config()
    config['default_bt'] = default_bt
    save_config(config)
