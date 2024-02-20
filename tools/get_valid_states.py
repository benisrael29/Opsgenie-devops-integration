import requests
import base64
import os
""" from dotenv import load_dotenv
load_dotenv() """

def get_and_print_work_item_states( work_item_type="Item"):
    """
    Retrieves and prints all valid states for a specific work item type in Azure DevOps.

    Args:
    pat (str): Personal Access Token for Azure DevOps.
    organization (str): The name of the organization in Azure DevOps.
    project (str): The name of the project in Azure DevOps.
    work_item_type (str): The work item type (e.g., "Bug", "Task").
    """
    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')
    headers = {
        'Authorization': f'Basic {encoded_pat}'
    }

    # Construct the URL for the API endpoint
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/workitemtypes/{work_item_type}/states?api-version=6.0"

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        states = response.json().get('value', [])
        print(f"Valid states for work item type '{work_item_type}':")
        for state in states:
            print(f"- {state['name']}")
    else:
        # Handle errors
        print(f"Failed to retrieve states. Status code: {response.status_code} Response: {response.text}")

# Example usage
get_and_print_work_item_states()