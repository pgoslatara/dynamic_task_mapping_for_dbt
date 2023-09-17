import logging
from typing import Sequence

from airflow.plugins_manager import AirflowPlugin
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)


class XebiaDbtPlugin(KubernetesPodOperator):
    template_fields: Sequence[str] = ("dbt_command",)

    def __init__(self, dbt_command: str, **kwargs):
        super().__init__(**kwargs)
        self.dbt_command = dbt_command

    def execute(self, context):
        logging.info(f"Running: {self.dbt_command}")

        self.arguments = [self.dbt_command]
        self.cmds = ["/bin/bash", "-c"]
        self.do_xcom_push = True  # Ensures sidecar pod is created to capture Xcom value
        self.image = "pgoslatara/dynamic-tasks:dbt-base"
        self.image_pull_policy = "Always"
        self.namespace = "default"
        self.startup_timeout_seconds = 450

        return super().execute(context)


class XebiaDbt(AirflowPlugin):
    name = "run_dbt_commands"
    operators = [XebiaDbtPlugin]
