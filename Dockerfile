FROM python:3.11.2-slim
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
RUN mkdir /srv/app
WORKDIR /srv/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./ /srv/app
# CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000"]
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000"]
