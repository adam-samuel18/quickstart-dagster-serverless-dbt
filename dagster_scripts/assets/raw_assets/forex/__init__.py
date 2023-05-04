from dagster import asset
import os
import subprocess

ENVIRONMENT = os.getenv("ENVIRONMENT")


@asset(compute_kind="python")
def fx_rates():
    cmd = (
        "python3 extract_and_load/scripts/fx_rates.py "
        f"--config fx_rates.json -env {ENVIRONMENT}"
    ).split()
    subprocess.run(cmd)
