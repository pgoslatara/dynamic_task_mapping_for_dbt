FROM python:3.11-slim

ARG DBT_SCHEMA
ARG GOOGLE_PROJECT_NAME

ENV DBT_SCHEMA ${DBT_SCHEMA}
ENV GOOGLE_PROJECT_NAME ${GOOGLE_PROJECT_NAME}

ENV DBT_PROFILES_DIR "./dbt_project"
ENV DBT_PROJECT_DIR "./dbt_project"

# Set working directory
RUN mkdir -p /dbt
WORKDIR /dbt

# Install OS dependencies
RUN apt-get update && apt-get install -qq -y \
    curl git --fix-missing --no-install-recommends

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:$POETRY_HOME/bin"

# Make sure we are using latest pip
RUN pip install --upgrade pip

# Install python dependencies
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install

# Copy repo code
COPY ./dbt_project ./dbt_project
RUN chmod +x ./dbt_project/scripts/extract_staging_paths.py

# Pre-install dbt packages and parse dbt project
RUN poetry run dbt deps && poetry run dbt parse

# dbt commands will be supplied from Airflow operator
CMD ["/bin/bash", "-c", "echo 'Expecting commands to be passed in.' && exit 1"]
