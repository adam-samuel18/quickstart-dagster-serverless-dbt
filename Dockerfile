FROM python:3.9-slim
RUN apt-get update && apt-get upgrade -yqq
RUN apt-get install git -y
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
WORKDIR /opt/dagster/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 3000
ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]