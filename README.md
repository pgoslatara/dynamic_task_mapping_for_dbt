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

1. Build the Docker image used for dbt:
    ```bash
    docker build --build-arg="DBT_SCHEMA=$DBT_SCHEMA" --build-arg="GOOGLE_PROJECT_NAME=$GOOGLE_PROJECT_NAME" --tag dbt-base:latest -f ./Dockerfile .
    ```

1. Test that the Docker image successfully builds dbt models:
    ```bash
    docker run --volume ~/.config/gcloud:/root/.config/gcloud -e DBT_SCHEMA=$DBT_SCHEMA -e GOOGLE_PROJECT_NAME=$GOOGLE_PROJECT_NAME -it --rm dbt-base:latest poetry run dbt build
    ```

1. Tag and push the Docker image:
    ```bash
    docker tag dbt-base:latest pgoslatara/dynamic-tasks:dbt-base
    docker push pgoslatara/dynamic-tasks:dbt-base
    ```

1. Install Minikube, steps [here](https://minikube.sigs.k8s.io/docs/start/).

1. Start a local Minikube cluster:
    ```bash
    minikube start --driver=docker
    ```

1. Enable the `gcp-auth` addon:
    ```bash
    minikube addons enable gcp-auth
    ```

1. [Optional] Enable all metrics and start the Minikube dashboard:
    ```bash
    minikube addons enable metrics-server
    minikube dashboard
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

To re-build your local dev environment, delete all files in `./dev` and repeat the above steps.

If you experience any issues with Minikube containers not authenticating to `gcloud` you can refresh the credentials:

```bash
minikube addons enable gcp-auth --refresh
```

# Talks

This repo accompanies the following talk:

* [Using Dynamic Task Mapping to Orchestrate dbt](https://airflowsummit.org/sessions/2023/using-dynamic-task-mapping-to-orchestrate-dbt/), slides available [here](https://docs.google.com/presentation/d/12tfwuZ8Z5oBugscxu9DVu__WrAaG0oiiEVPMpJMuwls/edit?pli=1#slide=id.p), recording available [here](https://www.youtube.com/watch?v=CjjZyxnHfdk).
