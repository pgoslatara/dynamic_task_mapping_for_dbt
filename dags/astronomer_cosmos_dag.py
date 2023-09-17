import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping

with DAG(
    dag_id="astronomer_cosmos",
    default_args={
        "owner": "Analytics Engineering",
        "retries": 3,
    },
    catchup=False,
    max_active_runs=1,
    concurrency=1,
    schedule=None,
    start_date=datetime(2023, 1, 1),
):
    dbt_tg = DbtTaskGroup(
        project_config=ProjectConfig(
            "./dbt_project",
        ),
        profile_config=ProfileConfig(
            profile_name="profiles",
            target_name="dev",
            profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
                conn_id="google_cloud_default",
                profile_args={
                    "project": os.environ["GOOGLE_PROJECT_NAME"],
                    "dataset": os.environ["DBT_SCHEMA"],
                    "method": "oauth",
                },
            ),
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path=str(
                (Path(os.environ["AIRFLOW_HOME"]) / ".." / ".venv/bin/dbt").absolute()
            ),
        ),
    )
