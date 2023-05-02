from dagster import ScheduleDefinition, define_asset_job

everything_job = define_asset_job("everything", selection="*")

schedules=[
    ScheduleDefinition(job=everything_job, cron_schedule="@daily"),
    ]