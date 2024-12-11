# Firestore CLI

This repository contains command-line tools for querying and updating Firestore collections.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/cdiddy77/firestore-cli.git
   cd firestore-cli
   ```

2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Usage

### Querying Firestore

The `fsquery.py` script allows you to query Firestore collections.

#### Command Line Arguments

- `--credentials`: Path to Firebase credentials JSON (optional, defaults to `GOOGLE_APPLICATION_CREDENTIALS` environment variable).
- `--path`: Path to Firestore collection (required).
- `--group`: Whether this is a group query (optional).
- `--where`: Query in the format `field:operation:value` (optional, can be used multiple times).
- `--id`: Query for a specific document ID (optional).
- `--orderby`: Field to order by, followed by `ASCENDING` or `DESCENDING` (optional, can be used multiple times).
- `--limit`: Limit the number of results (optional).

#### Example

```sh
poetry run python [fsquery.py](http://_vscodecontentref_/2) --path "your-collection-path" --where "field:==:value" --limit 10
```
