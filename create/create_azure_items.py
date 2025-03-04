
import json
import requests
import os
""" from dotenv import load_dotenv
load_dotenv() """
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
import re

def map_priority(opsgenie_priority):
    priority_map = {"P1": 1, "P2": 2, "P3": 3, "P4": 4, "P5": 4} 
    return priority_map.get(opsgenie_priority, 1)  # Default to 1 if not found

def format_title(alert_data):
    "Check for INC followed by at least 5 numbers is in the title. If not found, look for it in the descrption and add it to the start of the title"
    title = alert_data.get('message', '')
    if re.search(r'INC\d{4,}', title):
        return alert_data
    
    description = alert_data.get('description', '')

    match = re.search(r'INC\d{4,}', description)
    if match:
        alert_data['message'] = f"{match.group()} - {title}"
        return alert_data
    else:
        return alert_data



def create_azure_devops_work_item(alert_data, current_iteration, area_path=os.environ['AREA_PATH']):

    print("Alert data", alert_data)
    alert_data = format_title(alert_data)


    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')

    # Map Opsgenie priority to Azure DevOps priority
    priority = map_priority(alert_data.get('priority', 'P1'))

    priority = alert_data.get('priority', 1)
    if not isinstance(priority, int) or not (1 <= priority <= 5):
        priority = 1

    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/workitems/$Item?api-version=6.0"
    headers = {
        'Content-Type': 'application/json-patch+json',
        'Authorization': f'Basic {encoded_pat}'
    }

    body = [
        {"op": "add", "path": "/fields/System.AreaPath","value": area_path},
        {"op": "add", "path": "/fields/System.Title", "value": alert_data["message"]},
        {"op": "add", "path": "/fields/System.Description", "value": alert_data.get("description", "No description provided")},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority},
        {"op": "add", "path": "/fields/System.IterationPath", "value": current_iteration['path']},
        {"op": "add", "path": "/fields/System.Tags", "value": alert_data["alertId"]},

    ]
    response = requests.post(url, headers=headers, json=body)

    # Check for successful response
    if response.status_code == 200:
        print("Work item created successfully." )
        return response.json()
    else:
        # Handle errors
        print(f"Failed to create work item. Status code: {response.status_code} Response: {response.text}")
        return {"error": "Failed to create work item", "status_code": response.status_code, "details": response.text}

def create_alert_event(event, current_iteration):
    alert_data = event.get('alert', {})
    print("Alert data:", alert_data)

    # edit alert data priority to match Azure DevOps priority
    alert_data['priority'] = map_priority(alert_data.get('priority', 'P1'))

    # Create Azure DevOps work item
    response = create_azure_devops_work_item(alert_data, current_iteration)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }