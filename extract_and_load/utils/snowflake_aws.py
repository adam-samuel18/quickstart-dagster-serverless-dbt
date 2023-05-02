from aws import AWSSecretAuth
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas


class SnowflakeLoadAuth:
    def __init__(self, config: dict, env: str):
        if env == "dev":
            secret_name = "SF_LOAD_DEV"
        elif env == "prod":
            secret_name = "SF_LOAD_PROD"
        else:
            print("You must specify an environment in [dev, prod]")

        region_name = config["REGION_NAME"]
        self.aws_secret_auth = AWSSecretAuth(config)

        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        self.warehouse = config["WAREHOUSE"]

    def establish_connection(self) -> tuple(dict, str):
        secret = self.aws_secret_auth.get_secret()
        user = secret["user"]
        password = secret["password"]
        account = secret["account"]
        role = secret["role"]
        database = secret["database"]

        conn = sf.connect(
            user=user,
            password=password,
            account=account,
            role=role,
            warehouse=self.warehouse,
            database=database,
            schema=self.schema,
        )
        return conn, database


class SnowflakeExport:
    def __init__(self, config: dict, env: str):
        snowflake_load_auth = SnowflakeLoadAuth(config, env)
        self.conn, self.database = snowflake_load_auth.establish_connection()

    def copy_df_into_sf_table(self, result_dataframe) -> None:
        """
        Copies data into Snowflake table while not overwriting old data
        """
        success, nchunks, nrows, _ = write_pandas(
            self.conn, result_dataframe, self.table
        )
        self.conn.close
