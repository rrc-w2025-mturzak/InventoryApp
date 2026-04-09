import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Validate path parameters
    if (
        'pathParameters' not in event or
        'id' not in event['pathParameters'] or
        'location_id' not in event['pathParameters']
    ):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' or 'location_id' path parameter")
        }

    id_value = event['pathParameters']['id']
    location_id = Decimal(event['pathParameters']['location_id'])

    # Build the full composite key
    key = {
        'id': {'S': id_value},
        'location_id': {'N': str(location_id)}
    }

    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
