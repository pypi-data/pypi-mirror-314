import asyncio

from .config import env
from .session import Session


class SNS(Session):
    
    async def publish_messages_to_topic(self, topic_arn, messages, region=env.region):
        """
        Publish messages to a topic.
        :param topic_arn: The ARN of the topic.
        :param messages: The messages to publish.
        :param region: The region of the topic (default: us-east-1).
        :return: The response from the SNS API.
        """
        session = await self.session
        async with session.create_client(service_name="sns", region_name=region) as client:
            tasks = [client.publish(TopicArn=topic_arn, Message=message) for message in messages]
            responses = await asyncio.gather(*tasks)
        return responses
    
    async def publish_messages_with_attributes_to_topic(self, topic_arn, messages, region=env.region):
        """
        Publish messages with attributes to a topic.
        :param topic_arn: The ARN of the topic.
        :param messages: The messages to publish.
        :param region: The region of the topic (default: us-east-1).
        :return: The response from the SNS API.
        """
        session = await self.session
        async with session.create_client(service_name="sns", region_name=region) as client:
            tasks = [client.publish(TopicArn=topic_arn, Message=message["message"], MessageAttributes=message["attributes"]) for message in messages]
            responses = await asyncio.gather(*tasks)
        return responses
