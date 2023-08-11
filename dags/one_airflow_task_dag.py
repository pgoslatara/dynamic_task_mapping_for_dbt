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
    start_date=datetime(2023, 7, 1),
)
def one_airflow_task():
    BashOperator(
        bash_command="dbt build",
        task_id="dbt_build",
    )


one_airflow_task = one_airflow_task()
