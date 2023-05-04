from dagster import asset
from dagster_scripts.utils.constants import ENVIRONMENT
from extract_and_load.scripts.fx_rates import FXRates


@asset(compute_kind="python")
def fx_rates():
    fx_rates = FXRates("fx_rates.json", ENVIRONMENT)
    fx_rates.main()
