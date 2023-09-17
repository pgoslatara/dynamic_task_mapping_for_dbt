from datetime import datetime

from airflow import XComArg
from airflow.decorators import dag
from airflow.utils.task_group import TaskGroup
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
def dynamic_task_mapping():
    # Staging
    with TaskGroup(group_id="staging") as staging_models:
        determine_staging_paths = XebiaDbtPlugin(
            dbt_command="poetry run python ./dbt_project/scripts/extract_staging_paths.py",
            task_id="assemble_dbt_staging_commands",
        )

        # Works but  names unclear, can be improved once this Apache Airflow issue is resolved
        # https://github.com/apache/airflow/issues/22073
        dbt_build_staging = XebiaDbtPlugin.partial(
            task_id="dbt_build_staging",
        ).expand(dbt_command=XComArg(determine_staging_paths, key="return_value"))

    # Intermediate
    dbt_build_intermediate = XebiaDbtPlugin(
        dbt_command="poetry run dbt build --select intermediate",
        task_id="dbt_build_intermediate",
    )

    # Marts
    dbt_build_marts = XebiaDbtPlugin(
        dbt_command="poetry run dbt build --select marts",
        task_id="dbt_build_marts",
    )

    (staging_models >> dbt_build_intermediate >> dbt_build_marts)


dynamic_task_mapping = dynamic_task_mapping()
