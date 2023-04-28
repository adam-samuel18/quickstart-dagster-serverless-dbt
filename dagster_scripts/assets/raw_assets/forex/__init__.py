from dagster import asset
import subprocess

@asset(compute_kind="python")
def fx_rates():
    cmd = 'python3 extract_and_load/scripts/fx_rates.py --config fx_rates.json -env prod'.split()
    subprocess.run(cmd)