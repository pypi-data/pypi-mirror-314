# Simple DSSAT simulator


## Install
```
pipx install dssatsim
```

## Goal
Takes a small set of inputs in JSON and returns DSSAT's Summary.OUT as a JSON file.

### Required Set of Inputs:
```
{
    "farm_name": "farm_farm",
    "latitude": 42.4241716982,
    "longitude": -85.7411854356,
    "elevation": 200,
    "planting_date": "2023-05-15",
    "crop_name": "maize",
    "crop_variety": "Unknown",
    "is_irrigation_applied": "yes",
    "irrigation_application": [
        [
            "2023-05-15",
            80
        ],
        [
            "2023-05-20",
            100
        ]
    ]
}
```


## How to use it
```
from dssatsim import run_dssat_exp_cli
import json

input_file = "./sample_2024-09-30.json"
output_file = "./example_output.json"

with open(input_file, 'r', encoding='utf-8') as f:
    input_data = json.load(f)

_, explanations = run_dssat_exp_cli.exec(input_data, output_file)

```


## Limitations
* The geographic coverage is limited to Kalamazoo County, MI, USA
* Crops covered: Corn and Soybeans


## Acknowledgments

* [DSSAT Team](https://github.com/DSSAT/dssat-csm-os)
* [Py_DSSATTools](https://github.com/daquinterop/Py_DSSATTools)

