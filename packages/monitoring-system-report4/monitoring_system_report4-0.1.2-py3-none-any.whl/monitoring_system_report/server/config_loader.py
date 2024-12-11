import os

CONFIG_FILE = "./config.conf"

def load_config():
    config = {}
    if not os.path.exists(CONFIG_FILE):
        print(f"{CONFIG_FILE} not found!")
        return None

    with open(CONFIG_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=")
                config[key.strip()] = value.strip()


    return config
