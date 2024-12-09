import json
import asyncio
from decimal import Decimal

from functional import seq
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from .config import env
from .session import Session


serializer = TypeSerializer()
deserializer = TypeDeserializer()


class DynamoDB(Session):
    
    @staticmethod
    def preprocess_item(item):
        item = json.loads(json.dumps(item), parse_float=Decimal)
        try:
            item = {k: serializer.serialize(v) for k, v in item.items()}
        except AttributeError:
            return serializer.serialize(item)
    
    @staticmethod
    def process_item(item):
        return {k: serializer.serialize(v) for k, v in item.items()}
    
    async def describe_table(self, table_name, region=env.region):
        """
        Describe a DynamoDB table.
        :param table_name: The name of the table.
        :param region: The region of the table (default: us-east-1).
        :return: The response from the DynamoDB API.
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            response = await client.describe_table(
                TableName=table_name
            )
        return response
        
    async def put_items(self, table_name, items, region=env.region):
        """
        Put items into a DynamoDB table.
        :param table_name: The name of the table.
        :param items: The items to put.
        :param region: The region of the table (default: us-east-1).
        :return: The response from the DynamoDB API.
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            tasks = [client.put_item(
                TableName=table_name,
                Item=self.preprocess_item(item)
            ) for item in items]
            result = await asyncio.gather(*tasks)
        return result
    
    async def delete_items(self, table_name, id_list, region=env.region):
        """
        Delete items from a DynamoDB table.
        :param table_name: The name of the table.
        :param id_list: The IDs of the items to delete.
        :param region: The region of the table (default: us-east-1).
        :return: The response from the DynamoDB API.
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            tasks = [client.delete_item(
                TableName=table_name,
                Key=self.preprocess_item(id)
            ) for id in id_list]
            result = await asyncio.gather(*tasks)
        return result
    
    async def get_item(self, table_name, id, region=env.region):
        """
        Get an item from a DynamoDB table.
        :param table_name: The name of the table.
        :param id: The ID of the item to get.
        :param region: The region of the table (default: us-east-1).
        :return: The serialized item from the DynamoDB API.
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            response = await client.get_item(
                TableName=table_name,
                Key=self.preprocess_item(id)
            )
            result = self.process_item(response.get("Item", {}))
        return result
    
    async def get_items(self, table_name, id_list, region=env.region):
        """
        Get many items from a DynamoDB table.
        :param table_name: The name of the table.
        :param id_list: The IDs of the items to get.
        :param region: The region of the table (default: us-east-1).
        :return: The serialized items from the DynamoDB API.
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            tasks = [client.get_item(
                TableName=table_name,
                Key=self.preprocess_item(id)
            ) for id in id_list]
            response = await asyncio.gather(*tasks)
            result = [self.process_item(item.get("Item", {})) for item in response]
        return result
    
    async def index_query(self, table_mname, index, filters, region=env.region, **kwargs):
        """
        Get many items from a DynamoDB table using an index.
        :param table_mname: The name of the table.
        :param index: The index definition to query (example: {"name": "metadata-index", "field": "metadata", "value": "audio"}).
        :param filters: The filters to apply (example: {"deleted": false}).
        :param region: The region of the table (default: us-east-1).
        :param kwargs: Additional arguments to pass to the DynamoDB API.
        :return: The serialized items from the DynamoDB API.
        """
        
        filters.update({index["field"]: index["value"]})
        expression_attr = self.preprocess_item({f":{k}": filters[k] for k in filters.keys()})
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            response = await client.query(
                TableName=table_mname,
                IndexName=index["name"],
                KeyConditionExpression=f"#{index['field']} = :{index['field']}",
                ExpressionAttributeNames={f"#{index['field']}": index["field"]},
                ExpressionAttributeValues=expression_attr,
                **kwargs
            )
            result = [self.process_item(item) for item in response.get("Items", [])]
        return result
    
    async def scan_dynamo(self, table_name, region=env.region):
        """
        Scan a DynamoDB table.
        :param table_name: The name of the table.
        :param region: The region of the table (default: us-east-1).
        :return: The serialized items from the DynamoDB API
        """
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            response = await client.scan(
                TableName=table_name
            )
            result = list(seq(response.get("Items", [])).map(self.process_item))
            while "LastEvaluatedKey" in response:
                response = await client.scan(
                    TableName=table_name,
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                result.extend(list(seq(response.get("Items", [])).map(self.process_item)))
        return result
    
    async def update_items(self, table_name, items, key_fields, region=env.region):
        """
        Update items in a DynamoDB table.
        :param table_name: The name of the table.
        :param items: The items to update.
        :param key_fields: The fields to use as keys.
        :param region: The region of the table (default: us-east-1).
        :return: The serialized new items from the DynamoDB API.
        """
        
        items = [self.preprocess_item(item) for item in items]
        
        session = await self.session
        async with session.create_client(service_name="dynamodb", region_name=region) as client:
            tasks = [client.update_item(
                TableName=table_name,
                Key={k: item.pop(k) for k in key_fields},
                ReturnValues="ALL_NEW",
                AttributeValues={
                    **{k: {
                        "Action": "PUT",
                        "Value": v,
                    } for k, v in item.items()}}
            ) for item in items]
            response = await asyncio.gather(*tasks)
            result = [self.process_item(item.get("Attributes", {})) for item in response]
        return result