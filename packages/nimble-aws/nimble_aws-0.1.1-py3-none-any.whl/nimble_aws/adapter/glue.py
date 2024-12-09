import asyncio

from .config import env
from .session import Session


class Glue(Session):
    
    async def get_jobs(self, region=env.region):
        """
        Get a list of jobs.
        :param region: The region of the jobs (default: us-east-1).
        :return: The response from the Glue API.
        """
        session = await self.session
        async with session.create_client(service_name="glue", region_name=region) as client:
            response = await client.get_jobs()
        return response
    
    async def get_job_runs(self, job_name, max_results, region=env.region):
        """
        Get a list of job runs.
        :param job_name: The name of the job.
        :param max_results: The maximum number of results to return.
        :param region: The region of the job (default: us-east-1).
        :return: The response from the Glue API.
        """
        session = await self.session
        async with session.create_client(service_name="glue", region_name=region) as client:
            response = await client.get_job_runs(
                JobName=job_name,
                MaxResults=max_results
            )
        return response
    
    async def get_jobs_runs(self, job_names, max_results, region=env.region):
        """
        Get a list of job runs for multiple jobs.
        :param job_names: The names of the jobs.
        :param max_results: The maximum number of results to return.
        :param region: The region of the jobs (default: us-east-1).
        :return: The response from the Glue API.
        """
        session = await self.session
        async with session.create_client(service_name="glue", region_name=region) as client:
            tasks = [client.get_job_runs(
                JobName=job_name,
                MaxResults=max_results
            ) for job_name in job_names]
            response = await asyncio.gather(*tasks)
        return response