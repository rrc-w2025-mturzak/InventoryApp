import json
from decimal import Decimal

import boto3


def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = "Inventory"

    # Validate path parameters
    if (
        "pathParameters" not in event
        or "id" not in event["pathParameters"]
        or "location_id" not in event["pathParameters"]
    ):
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' or 'location_id' path parameter"),
        }

    id_value = event["pathParameters"]["id"]
    location_id = Decimal(str(event["pathParameters"]["location_id"]))  # CRITICAL FIX

    # Build the DynamoDB key
    key = {"id": {"S": id_value}, "location_id": {"N": str(location_id)}}

    try:
        dynamo_client.delete_item(TableName=table_name, Key=key)
        return {
            "statusCode": 200,
            "body": json.dumps(f"Item with ID {id_value} deleted successfully."),
        }
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps(f"Error deleting item: {str(e)}")}
