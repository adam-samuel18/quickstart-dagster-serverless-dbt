import os
import sys
from extract_and_load.utils.aws import AWSSecretAuth
from google.cloud import bigquery
from google.oauth2 import service_account

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class BigQueryLoadAuth:
    def __init__(self, config, env):
        if env == "dev":
            self.secret_name = "BIGQUERY_LOAD_DEV"
        elif env == "prod":
            self.secret_name = "BIGQUERY_LOAD_PROD"
        else:
            print("You must specify an environment in [dev, prod]")

        bigquery_secret_config = {
            "REGION_NAME": config["REGION_NAME"],
            "SECRET_NAME": self.secret_name,
        }

        secret_auth = AWSSecretAuth(bigquery_secret_config)
        self.service_account_creds = secret_auth.get_secret()
        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        self.warehouse = config["WAREHOUSE"]

    def establish_connection(self) -> tuple[str, dict]:
        # Construct a BigQuery client object.
        credentials = service_account.Credentials.from_service_account_info(
            self.service_account_creds
        )
        self.project_id = credentials.project_id
        self.client = bigquery.Client(
            credentials=credentials,
            project=self.project_id,
        )

        return self.project_id, self.client


class BigQueryExport:
    def __init__(self, config, env, job_config):
        bigquery_load_auth = BigQueryLoadAuth(config, env)
        (
            self.project_id,
            self.client,
        ) = bigquery_load_auth.establish_connection()
        self.table_id = f"{self.project_id}.{config['SCHEMA']}.{config['TABLE']}"
        self.job_config = job_config

    def copy_df_into_bq_table(self, df):
        """
        Copies data into Bigquery table while not overwriting old data
        """

        job = self.client.load_table_from_dataframe(
            df, self.table_id, job_config=self.job_config
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
            json, self.table_id, job_config=self.job_config
        )

        job.result()
        table = self.client.get_table(self.table_id)

        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), self.table_id
            )
        )
