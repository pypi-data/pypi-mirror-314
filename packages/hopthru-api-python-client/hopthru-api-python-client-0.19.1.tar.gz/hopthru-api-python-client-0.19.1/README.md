# Hopthru API Python Client

This is the Hopthru API Python Client for uploading APC data to Hopthru. 

It provides the interface for determining which dates Hopthru expects to receive data for, 
and for uploading data to Hopthru.

## Uploading Correlated APC Data

The following example shows how to upload correlated APC data to Hopthru.
```python
from hopthru_api_client import initialize_hopthru_api_client
from hopthru_api_client.apc_data import upload_correlated_apc_data
from hopthru_api_client.client import HOPTHRU_API_URL

AGENCY_NAME = 'example'
API_KEY = '<obtained from hopthru>'

def get_ridership(start_date, end_date) -> list[str]:
    # Implement agency-specific logic here.
    # It should write a CSV file to the path specified in output_filename.
    return "file_path.csv"

if __name__ == "__main__":
    options, config = initialize_hopthru_api_client()

    upload_correlated_apc_data(
        api_key=config["api_key"],
        apc_data_func=get_ridership,
        start_date=options.start_date,
        end_date=options.end_date,
        hopthru_api_url=config.get("api_url", HOPTHRU_API_URL),
        dry_run=options.dry_run,
    )
```

The upload_correlated_apc_data function handles command line arguments,
connects to the Hopthru API, and determines which date ranges need to be
uploaded. It then calls the get_ridership() function provided by the script
for each date range, and uploads the file it creates. And it logs the output
so the script can be run as a scheduled task.

## Uploading Raw APC Data

The following example shows how to upload raw APC data to Hopthru.
```python
from hopthru_api_client import initialize_hopthru_api_client
from hopthru_api_client.apc_data import upload_raw_apc_data
from hopthru_api_client.client import HOPTHRU_API_URL

def get_raw_ridership(start_date, end_date) -> list[str]:
    # Implement agency-specific logic here.
    # It should write a CSV file to the path specified in output_filename.
    return "file_path.csv"

if __name__ == "__main__":
    options, config = initialize_hopthru_api_client()

    upload_raw_apc_data(
        api_key=config["api_key"],
        apc_data_func=get_raw_ridership,
        start_date=options.start_date,
        end_date=options.end_date,
        hopthru_api_url=config.get("api_url", HOPTHRU_API_URL),
        dry_run=options.dry_run,
    )
```
By default, the upload_raw_apc_data function will query the Hopthru API for
the range of dates that need to be uploaded. It will then initiate the upload
and lastly perform the upload.

Alternatively, you can specify the start and end dates manually.


### Configuration

Configuration data should be stored in a file named `hopthru.ini` in the same directory.

```ini
[hopthru]
agency=<AGENCY_NAME>
api_key=<API_KEY_FROM_HOPTHRU>
log_file=log_file_name.txt
sentry_dsn=<SENTRY_DSN_FROM_HOPTHRU>
sentry_log_level=30
sentry_environment=prod
newrelic_api_key=<NEWRELIC_API_KEY_FROM_HOPTHRU>
```

## Building this package

- Create a virtual environment
    - `python -m venv venv`  
- Install the Python dependencies:
    - `python -m pip install --upgrade pip`
    - `python -m pip install -r test-requirements.txt`
- Build the distribution:
    - `python -m build`
- The distribution will be in the dist folder.


## Uploading the package to Pypi

```
twine upload dist/*
```