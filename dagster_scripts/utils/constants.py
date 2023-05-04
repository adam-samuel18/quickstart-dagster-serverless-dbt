from dagster._utils import file_relative_path

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt")
DBT_PROFILES_DIR = file_relative_path(__file__, "../../dbt")
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
