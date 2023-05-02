from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_project
from dagster_scripts.jobs import schedules
from dagster_scripts.assets.raw_assets import forex
from dagster_scripts.utils.constants import (
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    DBT_CONFIG,
)

raw_forex_assets = load_assets_from_package_module(
    forex,
    group_name="raw",
    key_prefix=["raw", "forex"],
)

dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    source_key_prefix=["raw"],
    key_prefix=["analytics", "dbt_schema"],
)

resources = {
    "dbt": dbt_cli_resource.configured(DBT_CONFIG),
}

defs = Definitions(
    assets=[*raw_forex_assets, *dbt_assets], resources=resources, schedules=schedules
)
