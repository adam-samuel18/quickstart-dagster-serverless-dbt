FROM python:3.8-slim
RUN apt-get update && apt-get upgrade -yqq && apt-get install git -y
ENV DAGSTER_HOME = /opt/dagster/app
RUN mkdir -p ${DAGSTER_HOME}
WORKDIR ${DAGSTER_HOME}
RUN pip install --upgrade pip

RUN python3 -m venv ${DAGSTER_HOME}/venv

COPY requirements.txt .
COPY dagster.yaml dagster_cloud.yaml workspace.yaml ${DAGSTER_HOME}/
RUN . $DAGSTER_HOME/venv/bin/activate
RUN pip install -r requirements.txt
RUN rm -rf requirements.txt /root/.cache