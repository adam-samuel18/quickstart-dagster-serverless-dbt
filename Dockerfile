FROM python:3.8-slim

RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y
ENV DAGSTER_HOME = /opt/dagster/app/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY dagster.yaml workspace.yaml requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt