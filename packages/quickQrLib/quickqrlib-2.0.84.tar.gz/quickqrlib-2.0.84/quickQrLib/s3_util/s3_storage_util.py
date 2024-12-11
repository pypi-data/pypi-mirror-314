from django.core.files.storage import default_storage
from django.conf import settings
import boto3

class S3StorageHelper:
    @staticmethod
    def get_default_storage():
        return default_storage
    
    @staticmethod
    def get_boto3_client():
        return boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION_NAME)
    
    @staticmethod
    def get_boto3_resource():
        return boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION_NAME)
    
    @staticmethod
    def create_bucket_name(bucket_name):
        return f"findIt-{bucket_name}"
    
    @staticmethod
    def create_s3_bucket(bucket_name):
        region = S3StorageHelper.get_bucket_region()
        bucket_name = S3StorageHelper.create_bucket_name(bucket_name)
        client = S3StorageHelper.get_boto3_client()
        response = client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        return bucket_name, response

    @staticmethod
    def get_bucket_name():
        return settings.AWS_STORAGE_BUCKET_NAME
    
    @staticmethod
    def get_bucket_url():
        return settings.AWS_S3_CUSTOM_DOMAIN
    
    @staticmethod
    def get_bucket_region():
        return settings.AWS_REGION_NAME
    
    @staticmethod
    def upload_file_to_s3(file_content, bucket_name, file_name, client, content_type):
        print(f"\nBucket Name: {bucket_name}\n")
        client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content, ContentType=content_type)
        return file_name
    
    @staticmethod
    def update_file_in_s3(file_content, bucket_name, file_name, client, content_type):
        client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content, ContentType=content_type)
        return file_name
    
    @staticmethod
    def delete_file_from_s3(file_name, client):
        bucket_name = S3StorageHelper.get_bucket_name()
        client.delete_object(Bucket=bucket_name, Key=file_name)

    @staticmethod
    def get_file_url(file_name):
        return f"{S3StorageHelper.get_bucket_url()}/{file_name}"
    
    @staticmethod
    def get_all_files_in_bucket(client):
        bucket_name = S3StorageHelper.get_bucket_name()
        response = client.list_objects(Bucket=bucket_name)
        return response.get('Contents', [])