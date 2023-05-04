FROM python:3.9-slim
RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY ./dagster_scripts ./dagster_scripts
COPY ./dbt ./dbt
COPY ./extract_and_load ./extract_and_load
COPY ./requirements.txt ./dagster_cloud.yaml ./dagster.yaml ./
RUN pip install -r requirements.txt
#RUN rm -rf requirements.txt /root/.cache