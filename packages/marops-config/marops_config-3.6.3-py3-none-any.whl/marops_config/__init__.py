# IMPORTANT
# After changing this file, run `python3 -m marops_config.generate_schemas`
# To re-generate the json schemas

from dataclasses import dataclass
from enum import Enum
from dacite import from_dict, Config
from typing import Any
from dataclasses import asdict
import yaml
import os
from pathlib import Path


MAROPS_CONFIG_FILE_NAME = "marops.yml"
MAROPS_SCHEMA_URL = "https://greenroom-robotics.github.io/marops/schemas/marops.schema.json"

@dataclass
class MarOpsConfig:
    # Should we start in production mode?
    prod: bool = False  
    # Should we use a secure cookie (only works with SSL)
    secure_cookie: bool = False
    # Path to where marops-data is stored
    data_path: str = "/tmp/marops-data"
    # Path to where backups are stored
    backup_path: str = "/etc/marops-backups"
    # Admin secret for Hasura
    hasura_admin_secret: str = "hasura-admin-secret"
    # Should we run a traefik reverse proxy
    proxy: bool = False
    # Host for the traefik reverse proxy
    proxy_host: str = "marops.greenroomrobotics.local"


def find_config() -> Path:
    """Returns the path to the .config/greenroom directory"""
    return Path.home().joinpath(".config/greenroom")


def dacite_to_dict(obj: Any):
    def dict_factory(data: Any):
        def convert_value(obj: Any):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return {k: convert_value(v) for k, v in data}

    return asdict(obj, dict_factory=dict_factory)


def get_path():
    return find_config() / MAROPS_CONFIG_FILE_NAME


def parse(config: dict[str, Any]) -> MarOpsConfig:
    return from_dict(
        MarOpsConfig,
        config,
        config=Config(cast=[]),
    )


def read() -> MarOpsConfig:
    path = get_path()
    with open(path) as stream:
        return parse(yaml.safe_load(stream))


def write(config: MarOpsConfig):
    path = get_path()
    # Make the parent dir if it doesn't exist
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w") as stream:
        print(f"Writing: {path}")
        headers = f"# yaml-language-server: $schema={MAROPS_SCHEMA_URL}"
        data = "\n".join([headers, yaml.dump(dacite_to_dict(config))])
        stream.write(data)
