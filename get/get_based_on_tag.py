import requests
import base64
import os

def query_work_items_by_tag(tag):
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/wiql?api-version=6.0"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}'
    }
    query = {
        "query": f"SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.Tags] CONTAINS '{tag}'"
    }
    response = requests.post(url, headers=headers, json=query)

    if response.status_code == 200:
        work_items = response.json()["workItems"]
        return work_items
    else:
        print(f"Failed to query work items by tag. Status code: {response.status_code} Response: {response.text}")
        return []

# Example usage
# Replace 'YourTagName' with the actual tag name you're filtering for
work_items = query_work_items_by_tag("e2fc53e3-9644-42f1-8218-bf3336065c01-1707370093454")
print(work_items)
