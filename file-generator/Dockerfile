FROM madnight/docker-alpine-wkhtmltopdf as wkhtmltopdf_image

FROM python:3.10-alpine

# Installing pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.3.1/pandoc-2.3.1-linux.tar.gz \
    && tar xvzf pandoc-2.3.1-linux.tar.gz --strip-components 1 -C /usr/local

# html to pdf engine
#RUN apk add  --no-cache --repository  http://dl-cdn.alpinelinux.org/alpine/v3.10/main/ wkhtmltopdf=0.12.5-r0
COPY --from=wkhtmltopdf_image /bin/wkhtmltopdf /bin/


WORKDIR /app

RUN pip install pipenv

COPY Pipfile.lock Pipfile.lock

RUN pipenv sync

COPY /app /app/app
WORKDIR /app/app
CMD pipenv run uvicorn main:app --host 0.0.0.0 --port 8080
RUN apk add --update --no-cache \
    libgcc libstdc++ libx11 glib libxrender libxext libintl \
    ttf-dejavu ttf-droid ttf-freefont ttf-liberation