from .config import env
from .session import Session


class AppSync(Session):
    
    async def list_keys(self, api_id, max_results=10, region=env.region):
        """
        List API keys.
        :param api_id: The ID of the API.
        :param max_results: The maximum number of results to return (default: 10).
        :param region: The region of the API (default: us-east-1).
        :return: The response from the AppSync API.
        """
        session = await self.session
        async with session.create_client(service_name="appsync", region_name=region) as client:
            response = await client.list_api_keys(
                apiId=api_id,
                maxResults=max_results
            )
            return response
        
    async def get_key(self, api_id, key_id, region=env.region):
        """
        Get an API key.service_name=
        :param api_id: The ID of the API.
        :param key_id: The ID of the key.
        :param region: The region of the API (default: us-east-1).
        :return: The value of the provided API key id.
        """
        session = await self.session
        async with session.create_client(service_name="appsync", region_name=region) as client:
            response = await client.list_api_keys(
                apiId=api_id,
                maxResults=100
            )
            api_key = next((key["id"] for key in response["apiKeys"] if key["id"] == key_id), response["apiKeys"][0]["id"])
            return api_key
        
    async def get_domain(self, api_id, region=env.region):
        """
        Get the domain name of an API.
        :param api_id: The ID of the API.
        :param region: The region of the API (default: us-east-1).
        :return: The domain name of the API.
        """
        session = await self.session
        async with session.create_client(service_name="appsync", region_name=region) as client:
            response = await client.list_graphql_apis()
            domain_name = next((domain["uris"]["GRAPHQL"] for domain in response["graphqlApis"] if domain["apiId"] == api_id), None)
            return domain_name
