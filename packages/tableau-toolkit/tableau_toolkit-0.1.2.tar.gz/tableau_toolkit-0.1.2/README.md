# Tableau Toolkit


## Dev Process

### Install Dependencies
poetry install

### Black to Standardize Code Formatting
poetry run black tableau_toolkit

### Pylint to Improve Code Readability
poetry run pylint tableau_toolkit

### Run cli commands
poetry run tt


### Build 
poetry build


### Publish
poetry config pypi-token.pypi <your-api-token> # do this only your first time
poetry publish # --skip-existing if adding a different platform build
