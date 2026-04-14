import json
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

    try:
        # 1. Query all items with this id
        query_response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression="id = :id",
            ExpressionAttributeValues={":id": {"S": id_value}}
        )

        items = query_response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps("No items found with that ID")
            }

        # 2. Delete each item using its real composite key
        for item in items:
            dynamo_client.delete_item(
                TableName=table_name,
                Key={
                    "id": {"S": item["id"]["S"]},
                    "location_id": {"N": item["location_id"]["N"]}
                }
            )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Deleted {len(items)} item(s) with ID {id_value}")
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }
