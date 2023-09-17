import json
import logging

from dbt.cli.main import dbtRunner


def assemble_dbt_staging_paths():
    res = dbtRunner().invoke(
        "dbt --quiet ls --resource-type model --select staging --output path".split(" ")[1:]
    )
    distinct_paths = {x[: x.rfind("/")] for x in res.result}
    logging.info(f"{distinct_paths=}")

    return [f"poetry run dbt build --select {x}" for x in list(distinct_paths)]


staging_paths = assemble_dbt_staging_paths()
logging.info(staging_paths)

# Write output to file so it is passed as Xcom
with open("/airflow/xcom/return.json", "w") as f:
    json.dump(staging_paths, f)
