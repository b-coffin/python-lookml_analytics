FROM python:3.12.1-bullseye

WORKDIR /src

EXPOSE 3001

RUN pip install jinja2 jmespath polars regex
