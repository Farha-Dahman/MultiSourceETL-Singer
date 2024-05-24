# Multi taps to one target

## Overview

MultiSourceETL-Singer is a Python project designed to extract, transform, and load data from multiple data sources into a MongoDB database. It is built as a [Singer](https://singer.io) tap, adhering to the Singer specification, to produce JSON-formatted data from various APIs and perform ETL operations.

This tap:
- Pulls raw data from multiple data sources
- Extracts data from various resources of each data source
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick start

1. **Install**

   We recommend using a virtual environment:

    ```bash
    # For macOS and Linux:
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > pip install your-package-name

    # For Windows:
    >  python -m virtualenv venv
    > venv\Scripts\activate
    > pip install your-package-name
    ```

2. **Create API Tokens / Access Credentials**

    Depending on the data sources you're integrating with, you may need to obtain API tokens or access credentials. Ensure you have the necessary permissions to access the data sources.

3. **Create the Configuration File**

    Create a JSON file `config.json` containing the necessary configuration parameters, including API tokens, data source endpoints, start dates, etc.

4. **Run the Tap in Discovery Mode to Generate Schema**

    Run the tap in discovery mode to generate the schema for each resource:

    ```bash
    your-tap-command --config config.json --discover > properties.json
    ```

5. **Select Streams to Sync**

    In the properties.json file, locate the metadata for each stream, usually found within a "schema" entry. To synchronize a stream, set "selected": true within the "schema" entry of that stream. For instance, to sync the collaborators stream:

    ```bash
    ...
    "stream": "collaborators",
    "metadata": [
    {
        "breadcrumb": [],
        "metadata": {
        "selected": true,
        "table-key-properties": [
            "id"
        ],
        "forced-replication-method": "FULL_TABLE",
        "inclusion": "available"
        }
    ...
    ```

6. **Run the Tap**

    Finally, run the tap with the configuration and properties files:

    ```bash
    your-tap-command --config config.json --properties properties.json
    ```

---
