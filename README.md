# Dynamic task mapping for dbt

A repo to demonstrate how to use [dynamic task mapping](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html) in Apache Airflow to orchestrate dbt. This example uses BigQuery and LocalExecutor.

## Local Setup

1. This repo uses [Poetry](https://python-poetry.org/docs/#installation) for package management, ensure Poetry is installed on your system.

1. Authenticate to GCP with [`gcloud`](https://cloud.google.com/sdk/docs/install):
    ```bash
    gcloud auth application-default login
    ```

1. Create a virtual environment and install required dependencies:
    ````bash
    poetry shell
    poetry install
    ```

1. Set the required environmental variables:
    ```bash
    export AIRFLOW_HOME="$(pwd)/dev"
    export AIRFLOW__CORE__DAGS_FOLDER="$(pwd)/dags"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/plugins"
    export AIRFLOW__CORE__PLUGINS_FOLDER="$(pwd)/plugins"
    export AIRFLOW__CORE__LOAD_EXAMPLES="False"

    export DBT_PROFILES_DIR="$(pwd)/dbt_project"
    export DBT_PROJECT_DIR="$(pwd)/dbt_project"
    export DBT_SCHEMA="<YOUR_SCHEMA>"
    export GOOGLE_PROJECT_NAME="<YOUR_GCP_PROJECT>"
    ```

1. Set the required Airflow variable:
    ```bash
    airflow db init
    airflow variables set DBT_PROJECT_DIR $(pwd)/dbt_project
    ```

1. Run dbt to generate the required `manifest.json` file:
    ```bash
    dbt build
    ```

1. Ensure your virtual environment is activated, start Airflow:
    ```bash
    airflow standalone
    ```

1. View the DAGs in the web UI at [http://localhost:8080](http://localhost:8080): username: `admin`, password can be found in `./standalone_admin_password.txt`.
