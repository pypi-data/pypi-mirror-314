from .config import env
from .session import Session


class Cognito(Session):
    
    async def get_user(self, auth, region=env.region):
        """
        Get a user.
        :param auth: The user's authentication token.
        :param region: The region of the user (default: us-east-1).
        :return: The response from the Cognito Identity Provider API.
        """
        session = await self.session
        async with session.create_client(service_name="cognito-idp", region_name=region) as client:
            response = await client.get_user(
                AccessToken=auth
            )
            return response