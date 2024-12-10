import pytest
from pathlib import Path
from gama_config.gama_vessel import (
    read_vessel_config,
    WaveflyerVesselConfig,
    Mode,
    Variant,
    LogLevel,
    Network,
    EducatVesselConfig,
)
from gama_config.test.helpers import write_temp_file


def test_read_vessel_config_works():
    config_string = "\n".join(
        [
            "variant: educat",
            "ros_domain_id: 0",
            "namespace_vessel: vessel_1",
            "namespace_groundstation: groundstation",
            "mode: simulator",
            "network: host",
            "prod: false",
            "log_level: info",
            "ubiquity_user: ''",
            "ubiquity_pass: ''",
            "ubiquity_ip: ''",
            "cameras: null",
            "record: false",
            "components:",
            "  autopilot:",
            "    pid: [1, 2, 3]",
            "advanced_configuration:",
            "  first_launch_arg: value",
            "  second_launch_arg: value",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_vessel_config(config_file)

    assert config == EducatVesselConfig(
        ros_domain_id=0,
        namespace_vessel="vessel_1",
        namespace_groundstation="groundstation",
        mode=Mode.SIMULATOR,
        network=Network.HOST,
        prod=False,
        log_level=LogLevel.INFO,
        cameras=None,
        record=False,
        components={
            "autopilot": {"pid": [1, 2, 3]},
        },
        advanced_configuration={"first_launch_arg": "value", "second_launch_arg": "value"},
    )


def test_throws_if_file_not_found():
    with pytest.raises(FileNotFoundError, match="Could not find config file"):
        read_vessel_config(Path("does_not_exist.yaml"))


def test_throws_if_file_cannot_be_parsed():
    config_file = write_temp_file("")

    with pytest.raises(ValueError, match="Could not parse config file"):
        read_vessel_config(config_file)


def test_throws_if_mode_does_not_match_enum():
    config_string = "\n".join(
        [
            "cameras: null",
            "log_level: info",
            "mode: goblin",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="Input should be 'simulator', 'hardware', 'stubs'"):
        read_vessel_config(config_file)


def test_throws_if_variant_does_not_match_enum():
    config_string = "\n".join(
        [
            "camera_overrides: null",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: killer-robot",
        ]
    )

    config_file = write_temp_file(config_string)

    with pytest.raises(
        ValueError,
        match=" Input tag 'killer-robot' found using 'variant' does not match any of the expected tags",
    ):
        read_vessel_config(config_file)


def test_throws_if_cameras_is_bad():
    config_string = "\n".join(
        [
            "cameras:",
            "- name: bow",
            "  order: 0",
            "  type: 89",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="Input should be a valid string"):
        read_vessel_config(config_file)


def test_throws_if_variant_specific_config_not_found():
    config_string = "\n".join(
        [
            "variant: waveflyer",
            "ros_domain_id: 0",
            "namespace_vessel: vessel_1",
            "namespace_groundstation: groundstation",
            "mode: simulator",
            "network: host",
            "prod: false",
            "log_level: info",
            "ubiquity_user: ''",
            "ubiquity_pass: ''",
            "ubiquity_ip: ''",
            "cameras: null",
            "record: false",
            "advanced_configuration:",
            "  random_launch_arg: value",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_vessel_config(config_file)

    assert config == WaveflyerVesselConfig(
        variant=Variant.WAVEFLYER,
        ros_domain_id=0,
        namespace_vessel="vessel_1",
        namespace_groundstation="groundstation",
        mode=Mode.SIMULATOR,
        network=Network.HOST,
        prod=False,
        log_level=LogLevel.INFO,
        cameras=None,
        record=False,
        components={},
        advanced_configuration={"random_launch_arg": "value"},
    )
