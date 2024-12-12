import boto3

dynamo_client = boto3.client('dynamodb', region_name="sa-east-1")
glue_client = boto3.client('glue', region_name="sa-east-1")
iam_client = boto3.client('iam', region_name="sa-east-1")
athena_client = boto3.client('athena', region_name="sa-east-1")
s3_client = boto3.client('s3', region_name="sa-east-1")