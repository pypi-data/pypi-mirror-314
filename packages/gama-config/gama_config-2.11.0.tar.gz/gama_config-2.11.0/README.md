# GAMA Config

GAMA Config is used to load config stored inside the `.gama` folder.

## Install

* `pip install -e ./libs/gama_config`
* or...
* `pip install gama_config` (Public on [PyPi](https://pypi.org/project/gama-config/))

## Usage

### Reading config

```python
from gama_config.gama_vessel import read_vessel_config
from gama_config.gama_gs import read_gs_config

vessel_config = read_vessel_config()
gs_config = read_gs_config()

```

### Writing config

```python
from gama_config.gama_vessel import write_vessel_config, GamaVesselConfig
from gama_config.gama_gs import write_gs_config, GamaGsConfig

vessel_config = GamaVesselConfig()
gs_config = GamaGsConfig()

write_vessel_config(vessel_config)
write_gs_config(gs_config)

```

### Generating schemas

After changing the dataclasses, you can generate the schemas with:

```bash
python3 -m gama_config.generate_schemas
```

## Running tests

```bash
python3 -m pytest -v ./libs/gama_config
```