# Importing a large dataset from a CSV to a database.

## Plan

I decided to use python and flask to accomplish the REST API part of this task.
This is mostly because I am familiar and like Flask and Python. It may not be the best tool, actually FastAPI or Falcon could probably be a little bit better for this simple application, and using Async TypeScript would probably be closer to the tooling I would choose for a production system, depnding on other factors like how often this task needs to run and what latency can be tollerated, vs development time and the likelihood ofrequiring to extend the functionality, and any other similar considerations. I think for a demonstration this will be a good setup.

I decided to use SQLAlchemy as the ORM as again, I am familiar with it and it's good enough for the task at hand. I will use Postgresql, no particular reason, i just usually opt for it given no other restrictions, but it is interchangeable by simple modifying the docker-compose file and the application config, given I will be using an ORM.

I went out of the assumption that what you would like to see is that I am able to handle long background tasks, and that it doesn't hold the application while the tasks are running, and that I am familiar with some of the techniques to accomplish those. 
There are a few options to demonstrate this, and between python's native threading and processing, or a more dedicated workload framework, I decided to go with Celery to perform the jobs as, and again, depending on many considerations, is probably closer to what a production system would use. Mostly, I believe that it'll better demonstrate that I understand the tradeoffs and tooling available for such jobs which is the main aim of this task. It's defintely an overkill for the task's requirements.

The reading of the CSV will be streaming, and I will break down the file into batches as this is how I would usually handle these tasks in the wild too. it's generally pefered over line by line importing and will be more efficient in terms of processing.

For testing, I will use pytest, as I usually do in all my python projects more or less.

If I have time and patience I will also write a github actions pipeline and a dummy terraform configurations

I will expose a bunch of endpoints, 

/health will do nothing accept return a 200 response, this is a good practice. I may add some actual application status information in it but i think it's not necessary as this is mostly to demonstrate that I know I should.

/import will accept a POST request which takes in a JSON payload containing a "target" key specifying the location of the CSV

/status/<job_id> will accept a GET and would return some statistic about the job, in principle this application can handle many jobs. If I have time and patience I may write a Jinja2 template that will periodically query that endpoint and display an updating progress information, as this was in the extras of this task

/abort/<job_id> will dispatch a message to celery to end a given job.

The application should be able to run by running `docker compose up` from the project's root directory.

These days, for these tasks, for initial motivations I would use ChatGPT to get me started, but in this case I don't think it's really very vecessary as I am already familiar enough with the tools and techniques I need to use. If i get lazy I may change my mind later but I don't think it's likely in this particular case.

## Implementation

1. I ended up consulting ChatGPT about a bunch of things, mostly related to Celery in the end.
2. I was planning to use python's built in `csv` to handle reading the file, but opted for pandas instead. Pandas feel like an overkill for this task and given i don't actually do any data analysis here it's not very sensible, but it has a convenient way of reading remote csv files in chunks. it's possible and not hard to achieve this using `requests` and `csv` too, and to remove the bloat associated with Pandas, but, i opted for this anyway in this case.
3. usually, for these tasks i try to start by writing unit tests, but in this case i will write the tests last. this is because the application does not have a lot of functions that lend themselves to be broken down to smaller units, it really only makes sense to write tests closer to integration tests, which test the flask endpoints and celery. the only real "unit" in this sense is parsing a CSV line into an SQLAlchemy model, the rest are pretty much all celery and flask functionality. I will write some integration tests, but this is not truly a TDD methodology (which I am a great advocate on usually).
4. Ok, after having finished everything, turned out, that despite what the internet and chat gpt thinks, pandas read_csv is not streaming, not even when using chunks. I had to reimplement the core function again. 
