# asterics_grid_api_v2

## Project Description

This project is the spiritual successor to https://github.com/Volskaar/asterics_grid_api_v1.git. It does not extend the mentioned projects functionality but is much rather a more functional extension of the original project https://github.com/asterics/AsTeRICS-Grid.git.

## Running the project locally

This project is based on the flask technology. To run it one must:
1. create a local python .venv \
````python -m venv .venv```` \
````Scripts/activate```` \
2. install the dependencies with requirements.txt\
````pip install -r requirements.txt````
3. run the flask application \
````flask --app main run````

## Preparations for dev_dumpProcessing
1. acquire the raw data dump (is roughly 500MB in size!) \
````curl -s https://kaikki.org/dictionary/downloads/de/de-extract.json > data.jso````