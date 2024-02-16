import json
import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
from dotenv import load_dotenv
load_dotenv()

from create.get.get_based_on_tag import query_work_items_by_tag



def add_comment_to_work_item(work_item_id, comment_text):
    # Encode the PAT for the header
    encoded_pat = base64.b64encode(bytes(':' + os.environ['PAT'], 'utf-8')).decode('ascii')

    # Construct the URL
    url = f"https://dev.azure.com/{os.environ['ORGANISATION']}/{os.environ['PROJECT']}/_apis/wit/workItems/{work_item_id}/comments?api-version=6.0-preview.3"

    # Set up the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}'
    }

    # Construct the body with the comment text
    body = {
        "text": comment_text
    }

    # Make the POST request to add the comment
    response = requests.post(url, headers=headers, json=body)

    # Check for successful response
    if response.status_code in [200, 201]:
        print("Comment added successfully.")
        return response.json()
    else:
        # Handle errors
        print(f"Failed to add comment. Status code: {response.status_code} Response: {response.text}")
        return {"error": "Failed to add comment", "status_code": response.status_code, "details": response.text}


def find_and_add_comment_to_work_item(tag, comment_text):
    # Find work items with the specified tag
    work_items = query_work_items_by_tag(tag)

    # Add a comment to each work item
    for work_item in work_items:
        work_item_id = work_item['id']
        add_comment_to_work_item(work_item_id, comment_text)

    

if __name__ == "__main__":
    add_comment_to_work_item(28227, "This is a test comment.")