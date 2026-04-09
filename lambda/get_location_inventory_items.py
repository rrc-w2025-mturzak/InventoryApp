import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "Inventory"


def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    # location_id comes from path parameters
    location_id = int(event["pathParameters"]["location_id"])

    try:
        response = table.scan(FilterExpression=Attr("location_id").eq(location_id))
        items = convert_decimals(response.get("Items", []))

        return {"statusCode": 200, "body": json.dumps(items)}

    except Exception as e:
        print(f"Failed to scan items: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("Failed to scan items")}
