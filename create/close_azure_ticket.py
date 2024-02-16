import json
import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
from dotenv import load_dotenv
load_dotenv()

import os
import base64
import requests

def close_azure_devops_work_item(work_item_id, closed_state='Done'):
    """
    Close an Azure DevOps work item by setting its state to the specified closed state.

    Args:
    work_item_id (int): The ID of the work item to close.
    closed_state (str): The state to set the work item to, indicating it is closed. Defaults to 'Done'.
    """
    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')

    # Construct the URL for updating the work item
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/workitems/{work_item_id}?api-version=6.0"

    headers = {
        'Content-Type': 'application/json-patch+json',
        'Authorization': f'Basic {encoded_pat}'
    }

    # Body to update the work item's state to the closed state
    body = [
        {"op": "add", "path": "/fields/System.State", "value": closed_state}
    ]

    # Send the PATCH request to update the work item
    response = requests.patch(url, headers=headers, json=body)

    # Check for successful response
    if response.status_code in [200, 204]:
        print("Work item closed successfully.")
        return response.json()
    else:
        # Handle errors
        print(f"Failed to close work item. Status code: {response.status_code} Response: {response.text}")
        return {"error": "Failed to close work item", "status_code": response.status_code, "details": response.text}

# Example usage:
# close_azure_devops_work_item(work_item_id=12345, closed_state='Done')
