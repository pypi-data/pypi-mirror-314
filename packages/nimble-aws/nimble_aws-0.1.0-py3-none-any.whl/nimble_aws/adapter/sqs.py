import json
import asyncio
from uuid import uuid4

from .config import env
from .session import Session
from .utils import chunk_array


class SQS(Session):
    
    @staticmethod
    def get_messages(result):
        return [json.loads(message["Body"]) for message in result.get("Messages", [])]
    
    async def publish_messages_to_queue(self, queue_url, messages, batch_size=10, region=env.region):
        """
        Publish messages to a queue.
        :param queue_url: The URL of the queue.
        :param messages: The messages to publish.
        :param batch_size: The number of messages to publish in a batch (default: 10).
        :param region: The region of the queue (default: us-east-1).
        :return: The response from the SQS API.
        """
        chunks = chunk_array(messages, batch_size)
        
        session = await self.session
        async with session.create_client(service_name="sqs", region_name=region) as client:
            tasks = [
                client.send_message_batch(
                    QueueUrl=queue_url,
                    Entries=[{"Id": str(uuid4()), "MessageBody": json.dumps(message)} for message in chunk]
                ) for chunk in chunks]
            responses = await asyncio.gather(*tasks)
        return responses

    async def read_ten_messages(self, queue_url, region=env.region, **kwargs):
        """
        Read ten messages from a queue.
        :param queue_url: The URL of the queue.
        :param region: The region of the queue (default: us-east-1).
        :return: The messages from the SQS API.
        """
        session = await self.session
        async with session.create_client(service_name="sqs", region_name=region) as client:
            response = await client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                **kwargs
            )
        return self.get_messages(response)
    

    async def read_messages(self, queue_url, num_messages=10, region=env.region, **kwargs):
        """
        Read messages from a queue.
        :param queue_url: The URL of the queue.
        :param num_messages: The number of messages to read (default: 10).
        :param region: The region of the queue (default: us-east-1).
        :return: The messages from the SQS API.
        """
        messages_read = 0
        all_messages = list()  
        messages = await self.read_ten_messages(queue_url, region, **kwargs)
        all_messages.extend(messages)
        messages_read += len(messages)
        while messages and messages_read < num_messages:
            messages = await self.read_ten_messages(queue_url, region, **kwargs)
            all_messages.extend(messages)
            messages_read += len(messages)
        return all_messages
    
    async def read_all_messages(self, queue_url, region=env.region, **kwargs):
        """
        Read all messages from a queue.
        :param queue_url: The URL of the queue.
        :param region: The region of the queue (default: us-east-1).
        :return: The messages from the SQS API.
        """
        all_messages = list()  
        messages = await self.read_ten_messages(queue_url, region, **kwargs)
        all_messages.extend(messages)
        while messages:
            messages = await self.read_ten_messages(queue_url, region, **kwargs)
            all_messages.extend(messages)
        return all_messages