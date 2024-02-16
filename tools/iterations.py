import requests
import base64
from datetime import datetime
import os

def get_current_iteration_data():
    """
    List all iteration paths for a given project and team in Azure DevOps.
    """
    # Encode the PAT for use in the header
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')
    headers = {'Authorization': f'Basic {encoded_pat}'}
    
    # Construct the URL for fetching iterations for the specified team and project
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/{os.environ['TEAM']}/_apis/work/teamsettings/iterations?api-version=6.0"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        iterations = response.json()
        for iteration in iterations['value']:
            if iteration['attributes']['timeFrame'] == 'current':
                return iteration
    else:
        print(f"Failed to fetch iterations. HTTP Status Code: {response.status_code}")


