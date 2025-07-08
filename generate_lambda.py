import boto3
import json
import uuid
from datetime import datetime

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ContentHistory")

def lambda_handler(event, context):
    body = json.loads(event["body"])
    keywords = body.get("keywords")

    prompt = f"\n\nHuman: Generate 5 creative marketing taglines about: {keywords}\n\nAssistant:"

    response = bedrock.invoke_model(
        modelId="anthropic.claude-instant-v1",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 200
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response['body'].read())['completion']

    item = {
        "Id": str(uuid.uuid4()),
        "Timestamp": datetime.utcnow().isoformat(),
        "InputKeywords": keywords,
        "GeneratedContent": result,
        "ModelUsed": "claude-instant-v1"
    }
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"result": result})
    }
