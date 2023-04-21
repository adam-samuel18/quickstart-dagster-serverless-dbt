# This script is made to collect foreign exchange rates (base: GBP) for various currencies.
# These will be the basis of calculations in our revenue models.

# We are using the forex_python package. Resulting exchange rates come back in a json format,
# however this needed a bit of modification to include the date passed to the function in the results.

# Results: some dates might be skipped, this will be dealt with later in the dbt models. Results are sent
# to S3 in json format.

import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

import json
import datetime
import argparse
import pandas as pd
from forex_python.converter import CurrencyRates
from extract_and_load.utils.get_dates import GetDates
#from extract_and_load.utils.snowflake_aws import SnowflakeExport
from extract_and_load.utils.duckdb_embedded import DuckDBExport


def get_report(daterange, base_currency):
    """
    Return foreign exchange rates for more than 25 currencies. Start and end date can be configured in the json config file.
    The entries come back per day, but there might be gaps. The date + exchange rates create a row, which are added to a list, this is the end result.
    """

    all_rows = []

    for date in daterange:
        try:
            daily_fx_rates = CurrencyRates().get_rates(
                base_currency,
                datetime.datetime(date.year, date.month, date.day),
            )
            row = {"date": date, "daily_fx_rates": daily_fx_rates}
            print(f"Retrieved foreign exchanges rates for: {date}")
            all_rows.append(row)
        except:
            pass

        all_rows_df = pd.DataFrame(all_rows)
    return all_rows_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Foreign Exchange Rates Pipeline")
    parser.add_argument("-c", "--config", required=True, help="a config json file")
    parser.add_argument(
        "-env",
        "--env",
        required=True,
        nargs="?",
        type=str,
        choices=["dev", "prod"],
        help="Define environment",
    )
    args = parser.parse_args()

    config = json.load(open("extract_and_load/configs/" + args.config))
    env = args.env

    get_dates = GetDates(config, env)
    daterange = get_dates.daterange()
    report = get_report(daterange, config['BASE_CURRENCY'])

    #snowflake_export = SnowflakeExport(config, env)
    #snowflake_export.copy_df_into_sf_table(report)

    duckdb_export = DuckDBExport()
    duckdb_export.view_df_into_ddb(report)