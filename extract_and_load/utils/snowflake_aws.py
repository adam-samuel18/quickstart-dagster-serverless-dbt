from aws import AWSSecretAuth
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas


class SnowflakeLoadAuth:

    def __init__(self, config, env):
        if env == 'dev':
            secret_name = 'SF_LOAD_DEV'
        elif env == 'prod':
            secret_name = 'SF_LOAD_PROD'
        else:
            print("You must specify an environment in [dev, prod]")

        region_name = config["REGION_NAME"]
        self.aws_secret_auth = AWSSecretAuth(config)

        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        self.warehouse = config["WAREHOUSE"]

    def establish_connection(self):

        secret = self.aws_secret_auth.get_secret()
        user = secret["user"]
        password = secret["password"]
        account = secret["account"]
        role = secret["role"]
        database = secret["database"]

        conn = sf.connect(
            user = user,
            password = password,
            account = account,
            role = role,
            warehouse = self.warehouse,
            database = database,
            schema = self.schema,
        )
        return conn, database

class SnowflakeExport:
    def __init__(self, config, env):

        snowflake_load_auth = SnowflakeLoadAuth(config, env)
        self.conn, self.database = snowflake_load_auth.establish_connection()

    def copy_df_into_sf_table(self, result_dataframe):
        """
        Copies data into Snowflake table while not overwriting old data
        """
        success, nchunks, nrows, _ = write_pandas(
            self.conn, result_dataframe, self.table
        )
        self.conn.close

    def merge_json_into_sf_table(self, sql = None):
        """
        Merges latest data into Snowflake table overwriting old rows
        """

        cur = self.conn.cursor()

        stmt = f"""
        MERGE INTO {self.database}.{self.schema}.{self.table} tbl USING
        (SELECT 
            METADATA$FILENAME AS FILENAME, 
            CONVERT_TIMEZONE('UTC', METADATA$FILE_LAST_MODIFIED) AS S3_LAST_MODIFIED_UTC
            $1:date AS DATE,
            $1 AS RAW_DATA
            FROM @{stage}( FILE_FORMAT => {file_format}) 
            WHERE S3_LAST_MODIFIED_UTC > (SELECT MAX(S3_LAST_MODIFIED_UTC) from {self.database}.{self.schema}.{self.table})
        ) stg ON tbl.DATE = stg.DATE
        WHEN MATCHED THEN
        UPDATE SET 
        FILENAME = stg.METADATA$FILENAME, 
        S3_LAST_MODIFIED_UTC = stg.CONVERT_TIMEZONE('UTC', METADATA$FILE_LAST_MODIFIED)
        RAW_DATA = stg.$1
        WHEN NOT MATCHED THEN
        INSERT
        (FILENAME, S3_LAST_MODIFIED_UTC, DATE, RAW_DATA) VALUES
        (stg.METADATA$FILENAME, 
        stg.CONVERT_TIMEZONE('UTC', METADATA$FILE_LAST_MODIFIED),
        stg.$1:date,
        stg.$1
        );
        """

        try:
            cur.execute(stmt)
        except sf.errors.ProgrammingError as e:
            print(e)
        finally:
            cur.close()

        self.conn.close
