# CSV Importer

A sample application to load a large CSV file into a Database. 

The input CSV format is [Jan 2024 High Volume For-Hire Vehicle Trip Records
(CSV)](https://public-vizz-storage.s3.amazonaws.com/backend/coding-challenges/large-file-importer/fhvhv_tripdata_2024-01.csv)

It is a flask application that utilises sqlalchemy and celery task queue because why make things easy for myself.

## Usage

### Docker Compose

on a good day, you should be able to simply start the application by running `docker compose up`. this will load some default settings and initiate a database and dependent services from configurations defined in `env.docker` and `config.py`. 

Once this is up, it opens 4 API endpoints, `/import` , `/status/<task-id>`, `/abort/<task-id>` and `/health`

By default the service listens for requests on port 8050


you can start the import process by running 

`curl  --header "Content-Type: application/json"  --request POST --data '{ "target": "https://public-vizz-storage.s3.amazonaws.com/backend/coding-challenges/large-file-importer/fhvhv_tripdata_2024-01.csv" }' localhost:8050/import` 

This will return the celery task ID, for example 

`{"task-id":"495d999c-032d-4fdc-a27b-2032f6814918"}`

you can query the number of records the worker has processed by using the `/status/` endpoint. for example

`curl localhost:8050/status/495d999c-032d-4fdc-a27b-2032f6814918`

You can also abort the job by hiting the `/abort/` endpoint with 
`curl localhost:8050/abort/495d999c-032d-4fdc-a27b-2032f6814918`

### Development 

For development, you may not want to rebuild the docker compose each time. there are a bunch of services that are required and can run in the background, while the main application, and the celery worker need to regularly be restarted.

you can start the background services, and they will be available for you to use by running the command

`docker compose up redis database mock-file-server`

There is a helper bash script to run this, `run_services.sh` which just does this

The first time you do this, you also need to run the database migration. you do this by running 

`docker compose up database-migrate`

**If you change the model, remember to run a migration by executing
`flask db migrate -m "Migration Name"`, and then run this again**

Next you need to setup the database connection environment. those need to match the ones in the env.docker file.

Create a `.env` file with this in it

```
POSTGRES_DB="rides"
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
```

You can then start the worker and the flask application locally by running 

`local_run.sh`

By default the application listens on port 5000, not 8050 like the docker compose method above.

You may not want to use the full CSV. there is an http server serving a truncated version bundled into the compose file. You can use this instead by running

`curl  --header "Content-Type: application/json"  --request POST --data '{ "target": "http://mock-file-server/mock-data.csv" }' localhost:5000/import`

> [!TIP]
> To check this worked, you can connect to the database by using
> `psql --host=localhost --username=user --dbname=rides`, with the password from abose
> and running `select count(*) from public.trips`

### Configurations

there are several configurations in the `config.py` py, and you can switch between them by setting the `ENVIRONMENT` environment variable.
currently only docker and local (default) are available, but there is a scaffolding for development, staging and production too and it is trivial to add more.
