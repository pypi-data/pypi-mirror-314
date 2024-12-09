import asyncio

from .config import env
from .session import Session


class EventBridge(Session):
    
    async def publish_events(self, messages, batch_size=10, region=env.region):
        """
        Publish events to an EventBridge bus.
        :param messages: The messages to publish.
        :param batch_size: The number of messages to publish at a time (default: 10).
        :param region: The region of the bus (default: us-east-1).
        :return: The response from the EventBridge API.
        """        

        chunks = [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]
        
        session = await self.session
        async with session.create_client(service_name="events", region_name=region) as client:
            tasks = [client.put_events(
                Entries=chunk
            ) for chunk in chunks]
            result = await asyncio.gather(*tasks)
        return result