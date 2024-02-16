import json
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
from dotenv import load_dotenv
load_dotenv()
from tools.iterations import get_current_iteration_data
from create.create_azure_items import create_alert_event
from create.create_azure_items import create_azure_devops_work_item
from create.create_azure_description import find_and_add_comment_to_work_item
from get.get_all_board_items import get_all_board_items

PAT = 'wse4nkmyc3dyx3ys3seecreeft5hxihhyp6k3h7aj2xi4df7jgpq'
ORGANISATION = 'dhapi-platform'
PROJECT = 'APIGW-Platform'
TEAM = 'Test'



def acknowledge_alert_event(event):
    # Implement acknowledge alert event
    find_and_add_comment_to_work_item(event['alertId'], 'Alert acknowledged')
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Acknowledged alert'})
    }


def close_alert_event(event):
    # Implement close alert event
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Closed alert'})
    }


def lambda_handler(event, context):
    # Extract alert data from Opsgenie event
    event_body = json.loads(event['body'])

    # Filter based on event type
    if event_body['action'] == 'Create':
        current_iteration = get_current_iteration_data()
        return create_alert_event(event_body, current_iteration)
    
    if event_body['action'] == 'Acknowledge':
        return acknowledge_alert_event(event_body)

    if event_body['action'] == 'Close':
        return close_alert_event(event_body)
    


def test():
    current_iteration = get_current_iteration_data()

    #get_all_board_items()
    create_azure_devops_work_item(alert_data={'alertId': 'e2fc53e3-9644-42f1-8218-bf3336065c01-1707370093454','message': 'TEST message', 'description': 'Test description', 'priority': 1},current_iteration=current_iteration)
    #find_and_print_current_iteration(ORGANISATION, PROJECT, TEAM, PAT)


if __name__ == "__main__":
    #get_current_iteration_data(ORGANISATION, PROJECT, PAT, TEAM)
    print(test())
    # lambda_handler(None, None)


