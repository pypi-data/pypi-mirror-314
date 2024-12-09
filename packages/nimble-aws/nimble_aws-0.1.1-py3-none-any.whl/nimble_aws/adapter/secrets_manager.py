import json

from .config import env
from .session import Session


class SecretsManager(Session):

    async def get_secret(self, secret_id, region=env.region):
        """
        Get a secret.
        :param secret_id: The ID of the secret.
        :param region: The region of the secret (default: us-east-1).
        :return: The requested secret id value.
        """
        session = await self.session
        async with session.create_client(service_name="secretsmanager", region_name=region) as client:
            response = await client.get_secret_value(SecretId=secret_id)
            secrets = json.loads(response["SecretString"])
        return secrets