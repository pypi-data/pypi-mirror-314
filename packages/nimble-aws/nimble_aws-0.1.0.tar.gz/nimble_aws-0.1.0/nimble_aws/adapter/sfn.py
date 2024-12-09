import json
import asyncio

from .config import env
from .utils import flatten
from .session import Session


class SFN(Session):
    
    async def run_sync_execution(self, state_machine_arn, payload, region=env.region):
        """
        Start an execution.
        :param state_machine_arn: The ARN of the state machine.
        :param input: The input to the execution.
        :param region: The region of the state machine (default: us-east-1).
        :return: The output from the Step Functions API.
        """
        session = await self.session
        async with session.create_client(service_name="stepfunctions", region_name=region) as client:
            response = await client.start_sync_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(payload)
            )
        return json.loads(response.get("output") or response.get("cause"))
    
    async def run_sync_executions(self, data, region=env.region):
        """
        Start multiple executions.
        :param data: The data to execute.
        :param region: The region of the state machine (default: us-east-1).
        :return: The output from the Step Functions API.
        """
        session = await self.session
        async with session.create_client(service_name="stepfunctions", region_name=region) as client:
            tasks = [client.start_sync_execution(stateMachineArn=item["arn"], input=json.dumps(item["input"])) for item in data]
            responses = await asyncio.gather(*tasks)
        return flatten([json.loads(response.get("output") or response.get("cause")) for response in responses])