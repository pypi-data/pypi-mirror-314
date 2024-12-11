import yaml
import os
from typing import Any, Callable
from pathlib import Path
import json

type_parse = Callable[[Any], Any]


class YamlDumper(yaml.Dumper):
    """
    A YAML dumpler that show lists on the same line if they do not contain dicts or list
    """

    def represent_sequence(self, tag, sequence, flow_style=None):
        if isinstance(sequence, list) and all(
            [not isinstance(item, (dict, list)) for item in sequence]
        ):
            flow_style = True
        return super().represent_sequence(tag, sequence, flow_style)

    def represent_mapping(self, tag, mapping, flow_style=None):
        flow_style = False
        return super().represent_mapping(tag, mapping, flow_style)


def join_lines(*lines: str) -> str:
    return "\n".join(lines)


def find_gama_config() -> Path:
    """Returns the path to the .gama directory"""
    return Path.home().joinpath(".config/greenroom")


def write_config(path: Path, config: Any, schema_url: str):

    # Make the parent dir if it doesn't exist
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w") as stream:
        print(f"Writing: {path}")
        headers = f"# yaml-language-server: $schema={schema_url}"
        data = "\n".join(
            [
                headers,
                yaml.dump(json.loads(config.model_dump_json()), Dumper=YamlDumper, sort_keys=True),
            ]
        )
        stream.write(data)


def serialise(obj: Any) -> str:
    return yaml.dump(obj.model_dump_json(), default_flow_style=True, sort_keys=True)

    return "woop"


def read_config(path: Path, parse: type_parse):
    try:
        with open(path) as stream:
            return parse(yaml.safe_load(stream))
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find config file: {path}")
    except Exception as e:
        raise ValueError(f"Could not parse config file {path} - {e}")
