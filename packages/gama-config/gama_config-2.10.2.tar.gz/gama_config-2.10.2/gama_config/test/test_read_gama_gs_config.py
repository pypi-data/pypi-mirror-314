import pytest
from pathlib import Path
from gama_config.gama_gs import read_gs_config, GamaGsConfig, Mode, LogLevel, Network
from gama_config.test.helpers import write_temp_file


def test_read_gs_config_works():
    config_string = "\n".join(
        [
            "vessel_ip: null",
            "log_level: info",
            "mode: none",
            "network: shared",
            "prod: false",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_gs_config(config_file)

    assert config == GamaGsConfig(
        log_level=LogLevel.INFO,
        mode=Mode.NONE,
        network=Network.SHARED,
        prod=False,
    )


def test_throws_if_file_not_found():
    with pytest.raises(FileNotFoundError, match="Could not find config file"):
        read_gs_config(Path("does_not_exist.yaml"))


def test_throws_if_file_cannot_be_parsed():
    config_file = write_temp_file("")

    with pytest.raises(ValueError, match="Could not parse config file"):
        read_gs_config(config_file)


def test_throws_if_mode_does_not_match_enum():
    config_string = "\n".join(
        [
            "vessel_ip: null",
            "log_level: info",
            "mode: goblin",
            "network: shared",
            "prod: false",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(
        ValueError,
        match="Input should be 'none', 'xbox', 'xbox_series_x', 'thrustmaster', 'thrustmaster_combo', 'warthog', 'warthog_combo', 'aeronav', 'single_unknown', 'dual_unknown', 'gladiator' or 'logitech_extreme'",
    ):
        read_gs_config(config_file)


def test_throws_if_network_does_not_match_enum():
    config_string = "\n".join(
        [
            "vessel_ip: null",
            "log_level: info",
            "mode: none",
            "network: starlink",
            "prod: false",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="Input should be 'shared' or 'host'"):
        read_gs_config(config_file)
