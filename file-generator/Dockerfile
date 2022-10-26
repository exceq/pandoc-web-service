FROM python:3.10-alpine

# Installing pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.3.1/pandoc-2.3.1-linux.tar.gz \
    && tar xvzf pandoc-2.3.1-linux.tar.gz --strip-components 1 -C /usr/local
RUN apk add texlive

WORKDIR /app

RUN pip install pipenv

COPY Pipfile.lock Pipfile.lock

RUN pipenv sync

CMD pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8080

COPY /app /app/app

