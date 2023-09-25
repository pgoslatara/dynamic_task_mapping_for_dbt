import os
from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import ExecutionMode, LoadMode

astronomer_cosmosv2 = DbtDag(
    catchup=False,
    dag_id="astronomer_cosmosv2",
    default_args={
        "owner": "Analytics Engineering",
        "retries": 3,
    },
    execution_config=ExecutionConfig(
        # dbt_executable_path=str(
        #     (Path(os.environ["AIRFLOW_HOME"]) / ".." / ".venv/bin/dbt").absolute()
        # ),
        execution_mode=ExecutionMode.KUBERNETES,
    ),
    max_active_runs=1,
    operator_args={
        "get_logs": True,
        "image": "pgoslatara/dynamic-tasks:latest",
        "is_delete_operator_pod": True,
    },
    project_config=ProjectConfig(
        dbt_project_path=(Path(os.environ["AIRFLOW_HOME"]) / ".." / "dbt_project").absolute(),
        manifest_path=(
            Path(os.environ["AIRFLOW_HOME"]) / ".." / "dbt_project/target/manifest.json"
        ).absolute(),
    ),
    profile_config=ProfileConfig(
        profile_name="profiles",
        target_name="dev",
        # profiles_yml_filepath=(Path(os.environ["AIRFLOW_HOME"]) / ".." / "dbt_project/profiles.yml").absolute(),
        # profiles_yml_filepath="."
    ),
    render_config=RenderConfig(
        # emit_datasets=True,
        load_method=LoadMode.DBT_MANIFEST,
        # select=["path:staging"]
    ),
    schedule=None,
    start_date=datetime(2023, 1, 1),
)
