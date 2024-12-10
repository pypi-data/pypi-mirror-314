# Hestia Engine Orchestrator

Orchestrate your different models to run on a Cycle, an ImpactAssessment or a Site.

## Documentation

Documentation can be found in the [source folder](./hestia_earth/orchestrator).

## Install

1. Install the library:
```bash
pip install hestia_earth.orchestrator
```

You can now install your own models or follow the steps below to use the default Hestia models.

### Install the Hestia Models

If you want to use the [hestia default models](/hestia-earth/hestia-engine-models), follow these steps:

1. Install the library:
```bash
pip install hestia_earth.models
```
2. Download the latest configuration files:
```bash
curl https://gitlab.com/hestia-earth/hestia-engine-orchestrator/-/raw/master/scripts/download_config.sh?inline=false -o download_config.sh && chmod +x download_config.sh
# pip default install directory is /usr/local/lib/python<version>/site-packages
./download_config.sh <pip install directory>
```

### Using your own models

You can create your own models in addition (or instead of) the default set of models provided by Hestia.

The model needs to expose only one method:
```python
def run(key: str, data): ...
```
It will be given the data that has been given to the orchestrator, i.e. by calling:
```python
from hestia_earth.orchestrator import run

my_data = {'@type': 'Cycle', 'inputs': []}
config = {
  "models": [{
    "key": "inputs",
    "model": "my_model",
    "value": "my_model_value",
    "runStrategy": "add_if_missing_key"
  }]
}
run(my_data, config)
```
Will be calling in your own model `my_model.py`:
```python
def run('my_model_value', my_data: dict): ...
```

### Usage

```python
# will work with either Cycle or Site
from hestia_earth.orchestrator import run

# cycle is a JSONLD node cycle
cycle = {'@type': 'Cycle', ...}
result = run(cycle, '/path/to/my-config.json')  # configuration stored in a file
print(result)
```
