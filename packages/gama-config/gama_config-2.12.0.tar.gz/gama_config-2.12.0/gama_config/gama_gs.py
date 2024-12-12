# IMPORTANT
# After changing this file, run `python3 -m gama_config.generate_schemas`
# To re-generate the json schemas

import os
import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum
from typing import Any, Optional
from gama_config import LogLevel
from gama_config.helpers import write_config, read_config, find_gama_config, serialise


GAMA_GS_FILE_NAME = "gama_gs.yml"
GAMA_GS_SCHEMA_URL = "https://greenroom-robotics.github.io/gama/schemas/gama_gs.schema.json"


class Variant(str, Enum):
    WHISKEY_BRAVO = "whiskey_bravo"
    EDUCAT = "educat"
    ORACLE_2_2 = "oracle_2_2"
    ORACLE_22 = "oracle_22"
    ARMIDALE = "armidale"
    WAVEFLYER = "waveflyer"
    DMAK = "dmak"
    MARS = "mars"

    def __str__(self):
        return self.value


class Mode(str, Enum):
    NONE = "none"
    XBOX = "xbox"
    XBOX_SERIES_X = "xbox_series_x"
    THRUSTMASTER = "thrustmaster"
    THRUSTMASTER_COMBO = "thrustmaster_combo"
    WARTHOG = "warthog"
    WARTHOG_COMBO = "warthog_combo"
    AERONAV = "aeronav"
    SINGLE_UNKNOWN = "single_unknown"
    DUAL_UNKNOWN = "dual_unknown"
    GLADIATOR = "gladiator"
    LOGITECH_EXTREME = "logitech_extreme"


class Network(str, Enum):
    SHARED = "shared"
    HOST = "host"


class GamaGsConfig(BaseModel):
    ros_domain_id: int = 0
    namespace_vessel: str = "vessel_1"
    namespace_groundstation: str = "groundstation"
    variant: Variant = Variant.ARMIDALE
    mode: Mode = Mode.NONE
    buttons: bool = False
    network: Network = Network.SHARED
    prod: bool = False
    log_level: LogLevel = LogLevel.INFO
    remote_cmd_override: bool = False
    simple_discovery: bool = False
    discovery_server_ip: str = Field(
        default="0.0.0.0",
        description="IP address of the discovery server. This should be the IP of the vessel.",
    )
    own_ip: str = Field(
        default="0.0.0.0",
        description="The IP address of the ground-stations's primary network interface. This is where DDS will bind to.",
    )


def parse_gs_config(config: dict[str, Any]) -> GamaGsConfig:
    # return from_dict(GamaGsConfig, config, config=Config(cast=[Mode, Network, LogLevel]))
    return GamaGsConfig(**config)


def get_gs_config_path():
    return find_gama_config() / GAMA_GS_FILE_NAME


def read_gs_config(path: Optional[Path] = None) -> GamaGsConfig:
    return read_config(path or get_gs_config_path(), parse_gs_config)


def read_gs_config_env() -> GamaGsConfig:
    gs_config_str = os.getenv("GAMA_GS_CONFIG")
    if gs_config_str is None:
        raise ValueError("GAMA_GS_CONFIG environment variable not set")
    return parse_gs_config(yaml.safe_load(gs_config_str))


def write_gs_config(config: GamaGsConfig):
    return write_config(get_gs_config_path(), config, GAMA_GS_SCHEMA_URL)


def serialise_gs_config(config: GamaGsConfig):
    return serialise(config)
