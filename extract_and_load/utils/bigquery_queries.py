import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from bigquery import BigQueryLoadAuth
from datetime import date, datetime


class BigQueryGetDates:
    def __init__(self, config, env):
        self.datetime_column = config["DATETIME_COLUMN"]
        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]

        bigquery_load_auth = BigQueryLoadAuth(config, env)
        self.database, self.client = bigquery_load_auth.establish_connection()

    def get_max_date_from_table(self) -> datetime:
        """
        Gets the maximum date in the table in the database
        """

        stmt = (f"select max({self.datetime_column}) from "
        f"{self.database}.{self.schema}.{self.table};")
        try:
            max_date_in_table_query = self.client.query(stmt)
            max_date_in_table = max_date_in_table_query.result()
            for date in max_date_in_table:
                max_date_in_table = date.values()[0]
                max_date_in_table = datetime.combine(
                    max_date_in_table, datetime.min.time()
                )

        except Exception as e:
            print(e)
            max_date_in_table = None
        print(f"max date in table = {max_date_in_table}")
        return max_date_in_table
