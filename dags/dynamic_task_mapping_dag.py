import logging
from datetime import datetime

from airflow import XComArg
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


def _assemble_dbt_build_commands(layer: str, source_task: str, **context):
    task_instance = context["task_instance"]
    xcom_output = task_instance.xcom_pull(task_ids=source_task)
    logging.info(f"{xcom_output=}")

    distinct_paths = list(
        {
            f"dbt build --select {x[:x.rfind('/')]}"
            for x in xcom_output.split(",")
            if x.find(f"models/{layer}") == 0
        }
    )
    logging.info(f"{distinct_paths=}")

    return distinct_paths


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
    retrieve_dbt_model_paths = BashOperator(
        bash_command="dbt --quiet ls --resource-type model --output path | paste -s -d, -",
        task_id="retrieve_dbt_model_paths",
    )

    # Staging
    with TaskGroup(group_id="staging") as staging_models:
        assemble_dbt_staging_commands = PythonOperator(
            op_kwargs={
                "layer": "staging",
                "source_task": "retrieve_dbt_model_paths",
            },
            python_callable=_assemble_dbt_build_commands,
            task_id="assemble_dbt_staging_commands",
        )

        # Works but task names unclear, can be improved once this Apache Airflow issue is resolved
        # https://github.com/apache/airflow/issues/22073
        dbt_build_staging = BashOperator.partial(
            task_id="dbt_build_staging",
        ).expand(bash_command=XComArg(assemble_dbt_staging_commands))

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

    (
        retrieve_dbt_model_paths
        >> assemble_dbt_staging_commands
        >> dbt_build_staging
        >> dbt_build_intermediate
        >> dbt_build_marts
    )


dynamic_task_mapping_dag = dynamic_task_mapping_dag()
