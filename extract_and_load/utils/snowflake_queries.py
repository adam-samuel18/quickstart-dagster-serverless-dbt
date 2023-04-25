import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import snowflake.connector as sf
from snowflake_aws import SnowflakeLoadAuth

class SnowflakeGetDates:
    def __init__(
        self, config: dict, env: str
    ):
        self.datetime_column = config["DATETIME_COLUMN"]
        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        
        snowflake_load_auth = SnowflakeLoadAuth(config, env)
        self.conn, self.database = snowflake_load_auth.establish_connection(self.schema)

    def get_max_date_from_table(self) -> datetime:
        """
        Gets the maximum date in the table in the database
        """
        cur = self.conn.cursor()
        stmt = f"select max({self.datetime_column}) from {self.database}.{self.schema}.{self.table};"
        try:
            max_date_in_table = cur.execute(stmt).fetchone()
        except sf.errors.ProgrammingError as e:
            print(e)
            max_date_in_table = None
        finally:
            cur.close()
            self.conn.close
        return max_date_in_table