import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
import logging
import datetime
import sys

# dynamodb settings
dynamodb_endpoint  = os.environ.get('DYNAMODB_ENDPOINT')
dynamodb_port = os.environ.get('DYNAMODB_PORT')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    if (dynamodb_endpoint is not None) and (dynamodb_port is not None):
        dynamodb = boto3.client('dynamodb',endpoint_url="http://" + dynamodb_endpoint + ":" + dynamodb_port)
    else:
        dynamodb = boto3.client('dynamodb')
except BotoCoreError as e:
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to DynamoDB succeeded")

landTableName = 'LandItems'

def AddItem(id):
    try:
        timestamp = datetime.datetime.now().isoformat()

        item = {
                'id': {'S': id},
                'size': {'N': '-1'},
                'detailed_location': {'S': ''},
                'description': {'S': ''},
                'price': {'S': ''},
                'gpt_response': {'S': ''},
                'created_at': {'S': timestamp},
                'modified_at': {'S': timestamp}
            }
        # write must come first to avoid race condition
        response = dynamodb.put_item(TableName=landTableName,Item=item,ConditionExpression="attribute_not_exists(id)")
    except ClientError as e:
        # Specifically catch the ConditionalCheckFailedException
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        else:
            raise Exception(f"An error occurred: {e}") from e
    return True

def UpdateItemProperties(id,size,location,description,price,gpt_response):
    try:
        # Prepare the update expression
        update_expression = "SET size = :new_size, detailed_location = :new_location, description = :new_description, price = :new_price,  gpt_response = :new_gpt_response"
        expression_attribute_values = {
            ':new_size': {'N': size},
            ':new_location': {'S': location},
            ':new_description': {'S': description},
            ':new_price': {'S': price},
            ':new_gpt_response': {'S': gpt_response}
        }

        # Update the item in the table
        response = dynamodb.update_item(
            TableName=landTableName,
            Key={'id': {'S': id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    except ClientError as e:
        raise Exception(f"An error occurred during item update: {e}") from e

    return response
