import json

from .config import env
from .session import Session


class ApiGateway(Session):
    
    async def post_to_connection(self, connection_id, data, region=env.region):
        """
        Send a message to a client's WebSocket connection.
        :param connection_id: The ID of the connection.
        :param data: The message to send.
        :param region: The region of the connection (default: us-east-1).
        :return: The response from the API Gateway Management API.
        """
        session = await self.session
        async with session.create_client("apigatewaymanagementapi", region_name=region) as client:
            response = await client.post_to_connection(
                ConnectionId=connection_id, 
                Data=json.dumps(data).encode("utf-8")
            )
            return response
    
    async def get_api_key(self, api_key_id, region=env.region):
        """
        Get an API key.
        :param api_key_id: The ID of the API key
        :param region: The region of the API key (default: us-east-1).
        :return: The response from the API Gateway API.
        """
        session = await self.session
        async with session.create_client("apigateway", region_name=region) as client:
            response = await client.get_api_key(
                apiKey=api_key_id,
                includeValue=True
            )
            return response