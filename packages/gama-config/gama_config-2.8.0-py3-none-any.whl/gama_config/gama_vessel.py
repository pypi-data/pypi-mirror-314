# IMPORTANT
# After changing this file, run `python3 -m gama_config.generate_schemas`
# To re-generate the json schemas

import os
import yaml
from pathlib import Path
from enum import Enum
from typing import Optional, Any, List, Union, Literal
from gama_config import LogLevel
from gama_config.helpers import write_config, read_config, find_gama_config, serialise
from greenstream_config.types import Camera
from pydantic import Field, BaseModel, ConfigDict, RootModel

GAMA_VESSEL_FILE_NAME = "gama_vessel.yml"
GAMA_VESSEL_SCHEMA_URL = (
    "https://greenroom-robotics.github.io/gama/schemas/gama_vessel.schema.json"
)


class Mode(str, Enum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"
    STUBS = "stubs"
    HITL_SIMULATOR = "hitl_simulator"

    def __str__(self):
        return self.value


class Network(str, Enum):
    SHARED = "shared"
    HOST = "host"

    def __str__(self):
        return self.value


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


class GamaVesselConfig(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            Variant: lambda v: v.value,
            Mode: lambda v: v.value,
            LogLevel: lambda v: v.value,
            Network: lambda v: v.value,
        },
    )

    variant: Variant
    ros_domain_id: int = Field(
        default=0,
        description="ROS domain ID for the vessel. This only applies if 'simple_discovery' is true.",
    )
    namespace_vessel: str = "vessel_1"
    namespace_groundstation: str = "groundstation"
    mode: Mode = Mode.SIMULATOR
    network: Network = Network.HOST
    prod: bool = False
    log_level: LogLevel = LogLevel.INFO
    cameras: Optional[List[Camera]] = None
    record: bool = False
    advanced_configuration: Optional[dict[str, str]] = None
    components: Any = Field(default_factory=dict)
    log_directory: str = "~/greenroom/gama/logs"
    charts_directory: str = "~/greenroom/charts"
    simple_discovery: bool = Field(
        default=False,
        description="Use simple discovery. This should NOT be used in production due to performance issues.",
    )
    with_discovery_server: bool = Field(
        default=True, description="Run the discovery server. It will bind to 0.0.0.0:11811"
    )
    discovery_server_ip: str = Field(
        default="0.0.0.0",
        description="IP/host/interface of the discovery server. Assumes port of 11811",
    )
    own_ip: str = Field(
        default="0.0.0.0",
        description="IP/host/interface address of the primary network interface. This is where DDS traffic will route to.",
    )


class ArmidaleVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.ARMIDALE] = Variant.ARMIDALE


class EducatVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.EDUCAT] = Variant.EDUCAT


class Oracle22VesselConfig(GamaVesselConfig):
    variant: Literal[Variant.ORACLE_22] = Variant.ORACLE_22


class Oracle2_2VesselConfig(GamaVesselConfig):
    variant: Literal[Variant.ORACLE_2_2] = Variant.ORACLE_2_2


class WaveflyerVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.WAVEFLYER] = Variant.WAVEFLYER


class WhiskeyBravoVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.WHISKEY_BRAVO] = Variant.WHISKEY_BRAVO


class DMAKVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.DMAK] = Variant.DMAK


class MarsVesselConfig(GamaVesselConfig):
    variant: Literal[Variant.MARS] = Variant.MARS


VariantVesselConfig = Union[
    ArmidaleVesselConfig,
    EducatVesselConfig,
    Oracle22VesselConfig,
    Oracle2_2VesselConfig,
    WaveflyerVesselConfig,
    WhiskeyBravoVesselConfig,
    DMAKVesselConfig,
    MarsVesselConfig,
]

DEFAULT_VARIANT_CONFIGS_MAP: dict[Variant, VariantVesselConfig] = {
    Variant.ARMIDALE: ArmidaleVesselConfig(),
    Variant.EDUCAT: EducatVesselConfig(),
    Variant.ORACLE_22: Oracle22VesselConfig(),
    Variant.ORACLE_2_2: Oracle2_2VesselConfig(),
    Variant.WAVEFLYER: WaveflyerVesselConfig(),
    Variant.WHISKEY_BRAVO: WhiskeyBravoVesselConfig(),
    Variant.DMAK: DMAKVesselConfig(),
    Variant.MARS: MarsVesselConfig(),
}


class VariantVesselConfigRoot(RootModel):
    root: VariantVesselConfig = Field(..., discriminator="variant")


def parse_vessel_config(config: Any) -> VariantVesselConfig:
    return VariantVesselConfigRoot(root=config).root


def get_vessel_config_path():
    return find_gama_config() / GAMA_VESSEL_FILE_NAME


def read_vessel_config(path: Optional[Path] = None) -> VariantVesselConfig:
    return read_config(path or get_vessel_config_path(), parse_vessel_config)


def read_vessel_config_env() -> VariantVesselConfig:
    config_str = os.environ.get("GAMA_VESSEL_CONFIG")
    if config_str is None:
        raise ValueError("GAMA_VESSEL_CONFIG environment variable not set")
    return parse_vessel_config(yaml.safe_load(config_str))


def write_vessel_config(config: GamaVesselConfig):
    return write_config(get_vessel_config_path(), config, GAMA_VESSEL_SCHEMA_URL)


def serialise_vessel_config(config: GamaVesselConfig):
    return serialise(config)
