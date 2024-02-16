
import json
import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
from dotenv import load_dotenv
load_dotenv()


def get_all_board_items(team='Test'):
    """
    Fetches all work items from an Azure DevOps board, including detailed information.

    :param organization: Azure DevOps organization name.
    :param project: Azure DevOps project name.
    :param pat: Personal Access Token with read permissions.
    :return: Detailed information for the work items.
    """
    # WiQL query URL
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/{team}/_apis/wit/wiql?api-version=6.0"
    print(url)

    # WiQL query to fetch all active work items (IDs only)
    query = {
        "query": "SELECT [System.Id], [System.Title], [System.AreaPath] FROM workitems WHERE [System.AssignedTo] = @me ORDER BY [System.CreatedDate] DESC" #[System.AreaPath] = 'APIGW-Platform\\Test' AND
    }

    # Headers for the WiQL query
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + os.environ['PAT']
    }

    #pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')

    # Make the WiQL query request
    response = requests.post(url, json=query, headers=headers, auth=HTTPBasicAuth('', os.environ['PAT']))

    if response.status_code == 200:
        work_item_ids = [item['id'] for item in response.json()['workItems']]
        detailed_work_items = []
        pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')

        # Fetch details for each work item ID
        for work_item_id in work_item_ids:
            details_url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/workitems/{work_item_id}?api-version=6.0&$expand=all"
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
    
if __name__ == "__main__":
    get_all_board_items()