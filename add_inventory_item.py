import json
import boto3
import uuid
import os
from decimal import Decimal

def lambda_handler(event, context):
    # Parse incoming JSON data with Decimal support
    try:
        data = json.loads(event['body'], parse_float=Decimal, parse_int=Decimal)
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'id': unique_id,
                'location_id': data['location_id'],   # now Decimal
                'description': data['description'],
                'name': data['name'],
                'price': data['price'],               # now Decimal
                'qty': data['qty']                    # now Decimal
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
