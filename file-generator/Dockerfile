FROM python:3.10-slim

RUN apt-get update && apt-get install -y wkhtmltopdf wget tar
# Installing pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.3.1/pandoc-2.3.1-linux.tar.gz
RUN tar xvzf pandoc-2.3.1-linux.tar.gz --strip-components 1 -C /usr/local

WORKDIR /app

RUN pip install pipenv

COPY Pipfile.lock Pipfile.lock

RUN pipenv sync

COPY /app /app/app
WORKDIR /app/app
CMD pipenv run uvicorn main:app --host 0.0.0.0 --port 8080
