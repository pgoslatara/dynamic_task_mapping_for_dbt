import logging
from datetime import datetime

from airflow import XComArg
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from dbt.cli.main import dbtRunner


def _assemble_dbt_staging_paths():
    res = dbtRunner().invoke(
        "dbt --quiet ls --resource-type model --select staging --output path".split(" ")[1:]
    )
    distinct_paths = {x[: x.rfind("/")] for x in res.result}
    logging.info(f"{distinct_paths=}")

    return [f"dbt build --select {x}" for x in list(distinct_paths)]


@dag(
    catchup=False,
    default_args={
        "retries": 3,
    },
    description="",
    max_active_runs=1,
    schedule=None,
    start_date=datetime(2023, 7, 1),
)
def dynamic_task_mapping_dag():
    # Staging
    with TaskGroup(group_id="staging") as staging_models:
        determine_staging_paths = PythonOperator(
            python_callable=_assemble_dbt_staging_paths,
            task_id="assemble_dbt_staging_commands",
        )

        # Works but task names unclear, can be improved once this Apache Airflow issue is resolved
        # https://github.com/apache/airflow/issues/22073
        dbt_build_staging = BashOperator.partial(
            task_id="dbt_build_staging",
        ).expand(bash_command=XComArg(determine_staging_paths))

        determine_staging_paths >> dbt_build_staging

    # Intermediate
    dbt_build_intermediate = BashOperator(
        bash_command="dbt build --select intermediate",
        task_id="dbt_build_intermediate",
    )

    # Marts
    dbt_build_marts = BashOperator(
        bash_command="dbt build --select marts",
        task_id="dbt_build_marts",
    )

    (staging_models >> dbt_build_intermediate >> dbt_build_marts)


dynamic_task_mapping_dag = dynamic_task_mapping_dag()
