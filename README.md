# Mars Habitability Explorer tools

The Mars Habitability Explorer is a standalone service that is intended to use different datasets to explore potentially habitable sites on Mars.

## Datasets

This has only been tested with the MOLA dataset so far. 

| Dataset | Size | Link|
|---------|------|--------------------------------------------------------------------------------|
| MOLA    | 2G   | https://planetarymaps.usgs.gov/mosaic/Mars_MGS_MOLA_DEM_mosaic_global_463m.tif |

## Installation

### Prerequisites

1. Python 3.8 or higher
2. Datasets to load
3. Access to the TkInter backend (others may be supported by accident)

### Virtual Environment and Libraries

Download the code and make a new environment for running

```bash
git clone https://github.com/mgoulish/mars-habitability-explorer.git
cd mars-habitability-explorer
python3 -m venv habitability
```

Install requisite libraries

```bash
source habitability/bin/activate 
pip install -r requirements.txt
```

## Running

The application uses a `config.json` file to figure out where the datasets are.
Download the datasets onto your computer and update the `config.json` file to point to the location of those datasets.

***Note*** Currently only MOLA is supported.

Activate the environment and run the code

```bash
source habitability/bin/activate 
python app.py
```

The app should pop up.
Click `Plot` to display the dataset.

***Note*** For MOLA it will take some time to display as it is a large dataset.

The plot space should be interactive and allow for zooming in and moving around.

When done, click `exit`.

