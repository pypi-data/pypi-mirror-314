import os
import yaml

def create_default_config():
    default_config = {
        "tableau_server": {"url": "https://hostname"},
        "authentication": {"type": "tableau_auth"},
        "personal_access_token": {
            "name": "name",
            "secret": "secret"
        },
        "tableau_auth": {"username": "username", "password": "password"},
        "site": {"content_url": ""},
        "api": {"version": "3.24"},
        "postgres": {
            "host": "host",
            "port": 8060,
            "database": "workgroup",
            "user": "readonly",
            "password": "password"
        }
    }

    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".tableau_toolkit")
    os.makedirs(config_dir, exist_ok=True)

    config_file_path = os.path.join(config_dir, "tableau.yaml")
    with open(config_file_path, "w") as config_file:
        yaml.dump(default_config, config_file, default_flow_style=False)

    return config_file_path
