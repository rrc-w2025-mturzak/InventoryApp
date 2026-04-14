import json
from decimal import Decimal
import boto3


def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = "Inventory"

    # Validate path parameter
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter"),
        }

    id_value = event["pathParameters"]["id"]

    # Build key using only id
    key = {"id": {"S": id_value}}

    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get("Item")

        if not item:
            return {"statusCode": 404, "body": json.dumps("Item not found")}

        return {"statusCode": 200, "body": json.dumps(item, default=str)}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps(str(e))}

#test