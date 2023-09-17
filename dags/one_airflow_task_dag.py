from datetime import datetime

from airflow.decorators import dag
from xebia_dbt import XebiaDbtPlugin


@dag(
    catchup=False,
    default_args={
        "owner": "Analytics Engineering",
        "retries": 3,
    },
    description="",
    max_active_runs=1,
    schedule=None,
    start_date=datetime(2023, 1, 1),
)
def one_airflow_task():
    XebiaDbtPlugin(
        task_id="dbt_build",
        dbt_command="poetry run dbt build",
    )


one_airflow_task = one_airflow_task()
