import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from datetime import datetime, timedelta
#from extract_and_load.utils.snowflake_queries import SnowflakeGetDates
from extract_and_load.utils.bigquery_queries import BigQueryGetDates

class GetDates:
    def __init__(
        self, config, env
    ):

        self.datetime_column = config["DATETIME_COLUMN"]
        self.number_of_days_to_ingest = config["NUMBER_OF_DAYS_TO_INGEST"] - 1
        self.first_import_from_date = config["FIRST_IMPORT_FROM_DATE"]
        self.schema = config["SCHEMA"]
        self.table = config["TABLE"]
        self.region_name = config["REGION_NAME"]
        self.from_date_override = config["FROM_DATE_OVERRIDE"]
        self.to_date_override = config["TO_DATE_OVERRIDE"]
        self.env = env
        self.config = config

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def get_dates(self, max_date_in_table = None):
        """
        Calculates the which dates to query when getting new raw data based on environment and max_date in the table
        """

        #snowflake_dates = SnowflakeGetDates(self.config, self.env)
        #max_date_in_table = snowflake_dates.get_max_date_from_table()
        bigquery_dates = BigQueryGetDates(self.config, self.env)
        max_date_in_table = bigquery_dates.get_max_date_from_table()

        if self.from_date_override == None:
            if self.env == 'dev':
                from_date = datetime.utcnow()-timedelta(days=7)
            elif self.env == 'prod':
                if max_date_in_table == None:
                    print(f'Doing initial import')
                    from_date = datetime.strptime(self.first_import_from_date,'%Y-%m-%d')
                else:
                    from_date = max_date_in_table - timedelta(
                        days=self.number_of_days_to_ingest
                    )
            else:
                print('env needs to be in [dev,prod]')
        else:
            from_date = self.from_date_override

        if self.to_date_override == None:
            to_date = datetime.utcnow()
        else:
            to_date = self.to_date_override

        print(f'Fetching data from {from_date} to {to_date}')

        return from_date, to_date

    def daterange(self):
        """
        Yields dates from the user defined daterange. The get_rates() function will work over these date values.
        :param start_date, end_date: are defined in the json config file
        """

        from_date, to_date = self.get_dates()

        for n in range(int((to_date - from_date).days)):
            yield from_date + timedelta(n)