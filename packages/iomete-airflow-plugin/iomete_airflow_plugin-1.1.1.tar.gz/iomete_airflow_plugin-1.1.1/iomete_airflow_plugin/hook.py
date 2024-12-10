from abc import ABC

from airflow.hooks.base import BaseHook
from airflow.models import Variable

from iomete_sdk.spark import SparkJobApiClient


class IometeHook(BaseHook, ABC):
    def __init__(
            self,
            variable_prefix: str = "iomete_",
    ):
        super().__init__()

        self.host = Variable.get(variable_prefix + "host")
        self.access_token = Variable.get(variable_prefix + "access_token")

        self.iom_client = SparkJobApiClient(
            host=self.host,
            api_key=self.access_token,
        )

    def submit_job_run(self, job_id, payload):
        response = self.iom_client.submit_job_run(job_id=job_id, payload=payload)
        return response

    def get_job_run(self, job_id, run_id):
        response = self.iom_client.get_job_run_by_id(job_id=job_id, run_id=run_id)
        return response

    def cancel_job_run(self, job_id, run_id):
        response = self.iom_client.cancel_job_run(job_id=job_id, run_id=run_id)
        return response
