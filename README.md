# Dagster Hybrid-Python-DBT-Lightdash
This repo contains a template for setting up a data pipeline using the following tools:
- Dagster Hybrid, for orchestration
- Python, for data ingestion
- DBT, for transformation
- Lightdash, for visualisation

A simple pipeline has been created whereby exchange rates are ingested into the data warehouse using
the forex python library. Then dbt is used to transform the data. Dimensions and metrics have been
defined in the marts layer so that they can be visualised in Lightdash.

There are three main folders in root:
- extract_and_load, contains all the python scripts, config files, and utils for ingesting the
exchange rates data
- dbt, contains the dbt transformations and tests
- dagster_scripts, contains scripts for creating the DAGs
