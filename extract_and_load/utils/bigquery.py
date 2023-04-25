import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from google.cloud import bigquery


class BigQueryLoadAuth:

    def __init__(self, config, env):
        if env == 'dev':
            self.project_name = 'raw-dev'
        elif env == 'prod':
            self.project_name = 'raw-prod'
        else:
            print("You must specify an environment in [dev, prod]")

        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        self.warehouse = config["WAREHOUSE"]

    def establish_connection(self) -> tuple[str, dict]:

        # Construct a BigQuery client object.
        self.client = bigquery.Client()

        return self.project_name, self.client


class BigQueryExport:
    def __init__(self, config, env, job_config):

        bigquery_load_auth = BigQueryLoadAuth(config, env)
        self.project_name, self.client = bigquery_load_auth.establish_connection()
        self.table_id = f"{self.project_name}.{config['SCHEMA']}.{config['TABLE']}"
        self.job_config = job_config

    def copy_df_into_bq_table(self, df):
        """
        Copies data into Bigquery table while not overwriting old data
        """

        job = self.client.load_table_from_dataframe(
            df, self.table_id, 
            job_config = self.job_config
        )

        job.result()
        table = self.client.get_table(self.table_id)

        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), self.table_id
            )
        )

    def copy_json_into_bq_table(self, json):
        """
        Copies data into Bigquery table while not overwriting old data
        """

        job = self.client.load_table_from_json(
            json, self.table_id, 
            job_config = self.job_config
        )

        job.result()
        table = self.client.get_table(self.table_id)

        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), self.table_id
            )
        )