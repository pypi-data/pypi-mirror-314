# Checker

`checker` is a Python package that helps prevent redundant downloads from Copernicus Marine datasets by leveraging MongoDB to check for duplicate requests.

## Installation

You can install the package using `pip`:

```bash
pip install checker==1.0.1

```
To use the duplication system for python api, import the following

```bash
in case of copernicusmarine
import copernicus_python_api

in case of cds
import cds_python_api
```

To use the duplication system for CLI, run the following commands

```bash
in case of copernicusmarine

python /path/to/copernicus_cli.py copernicusmarine subset --dataset-id ...

in case of ceda

python /path/to/ceda_cli.py wget ...

```