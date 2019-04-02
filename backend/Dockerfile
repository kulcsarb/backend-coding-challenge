FROM python:3.7-stretch
MAINTAINER Balázs Kulcsár <balazs.kulcsar@analogy.co>
LABEL version="0.1" \
    description="Backend challenge by Unbabel."

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* /app/

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .
RUN chmod +x wait-for-it.sh

EXPOSE 8000

