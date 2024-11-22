# CSV Importer

A sample application to load a large CSV file into a Database. 

The input CSV format is [Jan 2024 High Volume For-Hire Vehicle Trip Records
(CSV)](https://public-vizz-storage.s3.amazonaws.com/backend/coding-challenges/large-file-importer/fhvhv_tripdata_2024-01.csv)

## Usage

### Docker Compose

on a good day, you should be able to simply start the application by running `docker compose up`. this will load some default settings and initiate a database and dependent services from configurations defined in `env.docker` and `config.py`.

Once this is up, it opens 4 API endpoints, `/import` , `/status/<task-id>`, `/abort/<task-id>` and `/health`

you can start the import process by running 

`curl  --header "Content-Type: application/json"  --request POST --data '{ "target": "https://public-vizz-storage.s3.amazonaws.com/backend/coding-challenges/large-file-importer/fhvhv_tripdata_2024-01.csv" }' localhost:8050/import` 


