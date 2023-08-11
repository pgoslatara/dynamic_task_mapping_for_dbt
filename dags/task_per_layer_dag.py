from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator


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
def task_per_layer():
    dbt_build_staging = BashOperator(
        bash_command="dbt build --select staging",
        task_id="dbt_build_staging",
    )

    dbt_build_intermediate = BashOperator(
        bash_command="dbt build --select intermediate",
        task_id="dbt_build_intermediate",
    )

    dbt_build_marts = BashOperator(
        bash_command="dbt build --select marts",
        task_id="dbt_build_marts",
    )

    (dbt_build_staging >> dbt_build_intermediate >> dbt_build_marts)


task_per_layer = task_per_layer()
