# Dagster Hybrid-Python-DBT-Lightdash
This repo contains a template for setting up a data pipeline using the following tools:
- Dagster Hybrid (hosted on ECS), for orchestration
- Python, for data ingestion
- DBT, for transformation
- Lightdash, for visualisation

A simple pipeline has been created whereby exchange rates are ingested into the data warehouse using
the forex python library. Then dbt is used to transform the data. Dimensions and metrics have been
defined in the marts layer so that they can be visualised in Lightdash. The code has been written in
a way that separates dev and prod environments.

There are four main folders in root:
- extract_and_load, contains all the python scripts, config files, and utils for ingesting the
exchange rates data
- dbt, contains:
    - project.yml file, containing warehouse structure and model materialisations
    - source and model files
    - source and model tests
    - metrics and dimension definitions for visualisation in Lightdash
- dagster_scripts, contains scripts for creating the DAGs
- .github/workflows, contains workflows for:
    - linting dbt code using SQLFluff
    - linting python code using black & flake8
    - deploying to ECS
