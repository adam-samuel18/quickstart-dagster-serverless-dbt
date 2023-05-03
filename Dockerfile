FROM python:3.9-slim
RUN apt-get update && apt-get upgrade -yqq && apt-get install git -y
ENV DAGSTER_HOME = /opt/dagster/app/
ENV PATH = "/opt/venv/bin:$PATH"
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
RUN pip install --upgrade pip

COPY requirements.txt /opt/dagster/app/requirements.txt
COPY dagster.yaml dagster_cloud.yaml workspace.yaml /opt/dagster/app/
RUN ls
RUN pip install -r requirements.txt
RUN rm -rf requirements.txt /root/.cache