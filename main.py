import json
import requests
import base64

def map_priority(opsgenie_priority):
    priority_map = {"P1": 1, "P2": 2, "P3": 3, "P4": 4, "P5": 4}, 
    return priority_map.get(opsgenie_priority, 1)  # Default to 1 if not found


def create_azure_devops_work_item(pat, organization, project, alert_data):
    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

    # Map Opsgenie priority to Azure DevOps priority
    priority = map_priority(alert_data.get('priority', 'P1'))


    priority = alert_data.get('priority', 1)
    if not isinstance(priority, int) or not (1 <= priority <= 5):
        priority = 1

    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0"
    print(url)
    headers = {
        'Content-Type': 'application/json-patch+json',
        'Authorization': f'Basic {encoded_pat}'
    }
    body = [
        {"op": "add", "path": "/fields/System.Title", "value": alert_data["message"]},
        {"op": "add", "path": "/fields/System.Description", "value": alert_data.get("description", "No description provided")},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority},
        # Add more fields as needed
    ]
    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)

    # Check for successful response
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors
        return {"error": "Failed to create work item", "status_code": response.status_code, "details": response.text}

def create_alert_event(event):
    alert_data = event.get('alert', {})
    print("Alert data:", alert_data)

    azure_alert_data = {
        'message': alert_data.get('message', 'No message'),
        'description': alert_data.get('description', 'No description'),
        'priority': alert_data.get('priority', 'P1')  # Default to P1 if not provided
    }

    # Azure DevOps setup
    pat = 'oyfkyzkx3ushln34spfvqc4y3q2fiuvvkje5a4v5lyqn5z5bk24q'
    organization = 'dd-managed-services'
    project = 'Deloitte%20DevOps%20Services'

    # Create Azure DevOps work item
    response = create_azure_devops_work_item(pat, organization, project, azure_alert_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def acknowledge_alert_event(event):
    # Implement acknowledge alert event
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

    if event_body['action'] == 'Create':
        return create_alert_event(event_body)
    
    if event_body['action'] == 'Acknowledge':
        return acknowledge_alert_event(event_body)

    if event_body['action'] == 'Close':
        return close_alert_event(event_body)