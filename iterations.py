import requests
import base64
from datetime import datetime


def get_current_iteration_data(organization, project, pat, team):
    """
    List all iteration paths for a given project and team in Azure DevOps.
    """
    # Encode the PAT for use in the header
    encoded_pat = base64.b64encode(bytes(':' + pat, 'utf-8')).decode('ascii')
    headers = {'Authorization': f'Basic {encoded_pat}'}
    
    # Construct the URL for fetching iterations for the specified team and project
    url = f'https://dev.azure.com/{organization}/{project}/{team}/_apis/work/teamsettings/iterations?api-version=6.0'
    
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        iterations = response.json()
        for iteration in iterations['value']:
            print(iteration['name'], ":", iteration['path'], 'Start: ', iteration['attributes']['startDate'],'End date: ', iteration['attributes']['finishDate'])
            if iteration['attributes']['timeFrame'] == 'current':
                print('Current Iteration:', iteration['name'])
                print(iteration)
                return iteration
    else:
        print(f"Failed to fetch iterations. HTTP Status Code: {response.status_code}")



# Example usage
organization = 'dhapi-platform'
project = 'APIGW-Platform'
pat = 'wse4nkmyc3dyx3ys3seecreeft5hxihhyp6k3h7aj2xi4df7jgpq'
#team= 'Operate%20Team'


get_current_iteration_data(organization, project, pat, team)
