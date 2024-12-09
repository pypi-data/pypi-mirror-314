import asyncio
from botocore.client import Config

from .config import env
from .session import Session


class S3(Session):
    
    @staticmethod
    def extract_filename_from_files_list(files_list):
        return [f"{file['Name']}/{content['Key']}" for file in files_list for content in file["Contents"]]
    
    async def get_files(self, bucket, paths, decode=True, region=env.region):
        """
        Get a list of files from an S3 bucket.
        :param bucket: The name of the bucket.
        :param paths: The paths to the files.
        :param decode: Whether to decode the files (default: True).
        :param region: The region of the bucket (default: us-east-1).
        :return: The files.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.get_object(Bucket=bucket, Key=path) for path in paths]
            results = await asyncio.gather(*tasks)
            files = [await result["Body"].read() for result in results]
        return [file.decode("utf-8") for file in files] if decode else files
    
    async def list_files(self, bucket, prefix_list, region=env.region):
        """
        List files in an S3 bucket.
        :param bucket: The name of the bucket.
        :param prefix_list: The prefixes to list.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/") for prefix in prefix_list]
            results = await asyncio.gather(*tasks)
        return results
    
    async def put_file(self, bucket, key, body, region=env.region):
        """
        Put a file into an S3 bucket.
        :param bucket: The name of the bucket.
        :param key: The key of the file.
        :param body: The body of the file.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            response = await client.put_object(Bucket=bucket, Key=key, Body=body)
        return response

    async def put_files(self, bucket, objects, region=env.region):
        """
        Put files into an S3 bucket.
        :param bucket: The name of the bucket.
        :param objects: The objects to put.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.put_object(Bucket=bucket, Key=object["key"], Body=object["body"]) for object in objects]
            results = await asyncio.gather(*tasks)
        return results
    
    async def put_files_with_content_type(self, bucket, objects, region=env.region):
        """
        Put files into an S3 bucket with content type.
        :param bucket: The name of the bucket.
        :param objects: The objects to put.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.put_object(Bucket=bucket, Key=object["key"], Body=object["body"], ContentType=object["type"]) for object in objects]
            results = await asyncio.gather(*tasks)
        return results
    
    async def put_files_with_metadata(self, bucket, objects, region=env.region):
        """
        Put files into an S3 bucket with metadata.
        :param bucket: The name of the bucket.
        :param objects: The objects to put.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.put_object(Bucket=bucket, Key=object["key"], Body=object["body"], Metadata=object["metadata"]) for object in objects]
            results = await asyncio.gather(*tasks)
        return results
    
    async def head_files(self, bucket, keys, region=env.region):
        """
        Get the metadata of files in an S3 bucket.
        :param bucket: The name of the bucket.
        :param keys: The keys of the files.
        :param region: The region of the bucket (default: us-east-1).
        :return: The response from the S3 API.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region) as client:
            tasks = [client.head_object(Bucket=bucket, Key=key) for key in keys]
            results = await asyncio.gather(*tasks)
        return results
    
    async def generate_pre_signed_url(self, bucket, item, expiration, region=env.region):
        """
        Generate a pre-signed URL for a file in an S3 bucket.
        :param bucket: The name of the bucket.
        :param item: The item to generate a URL for.
        :param expiration: The expiration time of the URL.
        :param region: The region of the bucket (default: us-east-1).
        :return: The pre-signed URL.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region, config=Config(signature_version="s3v4")) as client:
            response = await client.generate_presigned_url(
                ClientMethod="get_object", 
                Params={
                    "Bucket": bucket, 
                    "Key": item["key"],
                    "ReponseContentDisposition": f"attachment; filename={item['name']}"
                }, 
                ExpiresIn=expiration
            )
        return response
    
    async def generate_pre_signed_urls(self, bucket, data, expiration, region=env.region):
        """
        Generate pre-signed URLs for files in an S3 bucket.
        :param bucket: The name of the bucket.
        :param data: The data to generate URLs for.
        :param expiration: The expiration time of the URLs.
        :param region: The region of the bucket (default: us-east-1).
        :return: The pre-signed URLs.
        """
        
        session = await self.session
        async with session.create_client(service_name="s3", region_name=region, config=Config(signature_version="s3v4")) as client:
            tasks = [
                client.generate_presigned_url(
                    ClientMethod="get_object", 
                    Params={
                        "Bucket": bucket, 
                        "Key": item["key"],
                        "ReponseContentDisposition": f"attachment; filename={item['name']}"
                    }, 
                    ExpiresIn=expiration
                ) for item in data]
            results = await asyncio.gather(*tasks)
        return results