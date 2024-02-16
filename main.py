import json
import os
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
from create.get.get_all_board_items import get_all_board_items
from create.close_azure_ticket import find_and_close_work_item_by_tag
PAT = 'wse4nkmyc3dyx3ys3seecreeft5hxihhyp6k3h7aj2xi4df7jgpq'
ORGANISATION = 'dhapi-platform'
PROJECT = 'APIGW-Platform'
TEAM = 'Test'



def acknowledge_alert_event(event):
    event_data= event['alert']
    comment = "Alert was acknowledged by " + event_data['username']
    # Implement acknowledge alert event
    find_and_add_comment_to_work_item(event_data['alertId'], comment)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Acknowledged alert'})
    }


def close_alert_event(event):
    event_data= event['alert']
    comment = "Alert was closed by " + event_data['username']
    find_and_close_work_item_by_tag(event_data['alertId'], comment=comment)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Closed alert'})
    }


def lambda_handler(event, context):
    # Extract alert data from Opsgenie event
    #event_body = json.loads(event['body'])
    event_body = event

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

def run_test_data_sets():
    # Define the path to the test data directory
    test_data_dir = 'test/data'
    
    # Explicitly define the order of processing
    order_of_processing = ['create_sample_data.json', 'ack_sample_data.json', 'close_sample_data.json']
    
    # Process files according to the defined order
    for filename in order_of_processing:
        # Construct the full file path
        file_path = os.path.join(test_data_dir, filename)
        
        # Check if the file exists to avoid errors
        if os.path.exists(file_path):
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Process the data (example: print it)
                print(f"Processing {filename}:")
                lambda_handler(data, None)
                print("\n---\n")
        else:
            print(f"File {filename} not found in {test_data_dir}")

# Call the function
if __name__ == "__main__":
    run_test_data_sets()

