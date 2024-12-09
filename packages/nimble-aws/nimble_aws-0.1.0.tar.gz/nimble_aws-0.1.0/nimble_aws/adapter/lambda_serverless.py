import json

from .config import env
from .session import Session


class Lambda(Session):
    
    async def invoke(self, function_name, payload, invocation_type="RequestResponse", region=env.region):
        """
        Invoke a Lambda function.
        :param function_name: The name of the function.
        :param payload: The payload to send to the function.
        :param invocation_type: The invocation type, valid values are Event | RequestResponse | DryRun (default: RequestResponse).
        :param region: The region of the function (default: us-east-1).
        :return: The response payload from the Lambda API.
        """
        session = await self.session
        async with session.create_client("lambda", region_name=region) as client:
            response = await client.invoke(
                FunctionName=function_name,
                InvocationType=invocation_type,
                Payload=json.dumps(payload).encode("utf-8")
            )
        return json.loads(response["Payload"].read().decode("utf-8")) if invocation_type == "RequestResponse" else response["Payload"].read()
    