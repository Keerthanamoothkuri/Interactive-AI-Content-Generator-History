# backend/history_lambda.py

import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ContentHistory")

def lambda_handler(event, context):
    response = table.scan()
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"items": response["Items"]})
    }
