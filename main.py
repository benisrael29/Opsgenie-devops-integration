import json
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
from iterations import get_current_iteration_data

PAT = 'wse4nkmyc3dyx3ys3seecreeft5hxihhyp6k3h7aj2xi4df7jgpq'
ORGANISATION = 'dhapi-platform'
PROJECT = 'APIGW-Platform'
TEAM = 'Test'


def map_priority(opsgenie_priority):
    priority_map = {"P1": 1, "P2": 2, "P3": 3, "P4": 4, "P5": 4} 
    return priority_map.get(opsgenie_priority, 1)  # Default to 1 if not found

def create_azure_devops_work_item(pat, organization, project, alert_data, area_path='APIGW-Platform\\Test'):
    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

    # Map Opsgenie priority to Azure DevOps priority
    priority = map_priority(alert_data.get('priority', 'P1'))

    # Get current iteration data
    current_iteration = get_current_iteration_data(organization, project, pat, TEAM)

    priority = alert_data.get('priority', 1)
    if not isinstance(priority, int) or not (1 <= priority <= 5):
        priority = 1

    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Item?api-version=6.0"
    print(url)
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

        # Add more fields as needed
    ]
    response = requests.post(url, headers=headers, json=body)
    print(response.status_code)

    # Check for successful response
    if response.status_code == 200:
        print("Work item created successfully.")
        return response.json()
    else:
        # Handle errors
        print(f"Failed to create work item. Status code: {response.status_code} Response: {response.text}")
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

    # Create Azure DevOps work item
    response = create_azure_devops_work_item(PAT, ORGANISATION, PROJECT, azure_alert_data)
    
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



def get_all_board_items(organization, project, pat,team='Test'):
    """
    Fetches all work items from an Azure DevOps board, including detailed information.

    :param organization: Azure DevOps organization name.
    :param project: Azure DevOps project name.
    :param pat: Personal Access Token with read permissions.
    :return: Detailed information for the work items.
    """
    # WiQL query URL
    url = f'https://dev.azure.com/{organization}/{project}/{team}/_apis/wit/wiql?api-version=6.0'
    print(url)

    # WiQL query to fetch all active work items (IDs only)
    query = {
        "query": "SELECT [System.Id], [System.Title], [System.AreaPath] FROM workitems WHERE [System.AreaPath] = 'APIGW-Platform\\Test' AND [System.AssignedTo] = @me ORDER BY [System.CreatedDate] DESC" #[System.AreaPath] = 'APIGW-Platform\\Test' AND
    }

    # Headers for the WiQL query
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + pat
    }

    #pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

    # Make the WiQL query request
    response = requests.post(url, json=query, headers=headers, auth=HTTPBasicAuth('', pat))

    if response.status_code == 200:
        work_item_ids = [item['id'] for item in response.json()['workItems']]
        detailed_work_items = []
        pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

        # Fetch details for each work item ID
        for work_item_id in work_item_ids:
            details_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=6.0&$expand=all'
            details_response = requests.get(details_url, headers={'Authorization': 'Basic ' + pat})

            if details_response.status_code == 200:
                detailed_work_items.append(details_response.json())
                print(details_response.json())
            else:
                print(f"Failed to fetch details for work item ID {work_item_id}.")
        
        print("Work item details fetched successfully.")
        print('Returned :',len(detailed_work_items) , ' items')
        return detailed_work_items
    else:
        print("Failed to fetch work item IDs.")
        print(response.status_code)
        return None


def find_and_print_current_iteration(organization, project, pat, team='Operate%20Team'):
    # API endpoint to get iterations for a team
    url = f'https://dev.azure.com/{organization}/{project}/{team}/_apis/work/teamsettings/iterations?api-version=6.0'
    #pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

    # Prepare the headers for authentication
    headers = {'Authorization': f'Basic {pat}'}
    
    # Function to convert date string to datetime object
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

    # Function to find the current iteration
    def find_current_iteration(iterations):
        current_date = datetime.now()
        for iteration in iterations:
            start_date = parse_date(iteration['attributes'].get('startDate'))
            end_date = parse_date(iteration['attributes'].get('finishDate'))
            if start_date and end_date and start_date <= current_date <= end_date:
                return iteration
        return None

    # Make the request to the Azure DevOps API
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        iterations_data = response.json()
        print(iterations_data)
        current_iteration = find_current_iteration(iterations_data['value'])
        if current_iteration:
            print(f"Current iteration: {current_iteration['name']}")
        else:
            print("No current iteration found.")
    else:
        print(f"Failed to fetch iterations. HTTP Status Code: {response.status_code}")


def lambda_handler(event, context):
    # Extract alert data from Opsgenie event
    event_body = json.loads(event['body'])

    # Filter based on event type
    if event_body['action'] == 'Create':
        return create_alert_event(event_body)
    
    if event_body['action'] == 'Acknowledge':
        return acknowledge_alert_event(event_body)

    if event_body['action'] == 'Close':
        return close_alert_event(event_body)
    


def test():
    get_all_board_items(ORGANISATION, PROJECT, PAT)
    #create_azure_devops_work_item(PAT, ORGANISATION, PROJECT, {'message': 'TEST message', 'description': 'Test description', 'priority': 1})
    #find_and_print_current_iteration(ORGANISATION, PROJECT, TEAM, PAT)


if __name__ == "__main__":
    print(test())
    # lambda_handler(None, None)


