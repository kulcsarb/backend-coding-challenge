FROM python:3.7-stretch
MAINTAINER Balázs Kulcsár <balazs.kulcsar@analogy.co>
LABEL version="0.1" \
    description="Backend challenge by Unbabel."

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY translator translator

EXPOSE 8000

