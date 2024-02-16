# Opsgenie to Azure DevOps Integration

This repository contains the codebase for an integration solution between Opsgenie and Azure DevOps, designed to automate the alert management process. The solution facilitates the creation, acknowledgment, and closure of Azure DevOps work items based on alerts from Opsgenie.

## Overview

The integration is implemented in Python and is intended to be deployed as an AWS Lambda function. It listens for webhook events from Opsgenie, processes these events, and performs corresponding actions in Azure DevOps, such as creating work items, adding comments, or closing work items.

## Features

- **Create Alert Event**: Converts Opsgenie alerts into Azure DevOps work items.
- **Acknowledge Alert Event**: Adds a comment to a work item in Azure DevOps when an alert is acknowledged in Opsgenie.
- **Close Alert Event**: Closes a work item in Azure DevOps when an alert is closed in Opsgenie.

## Prerequisites

Before you begin, ensure you have the following:

- An Azure DevOps account with access to a project where work items will be created.
- An Opsgenie account with permissions to create and manage alerts.
- AWS account with permissions to create and manage Lambda functions.
- `python3` and `pip` installed on your local machine for testing.

## Setup Instructions

### 1. Clone the Repository

Start by cloning this repository to your local machine or directly to your cloud development environment.

### 2. Environment Variables

The integration requires setting up environment variables to securely store and access credentials. Create a `.env` file in the root of the project with the following contents:

```
ADHA_DEVOPS_KEY=YourAzureDevOpsAccessKey
URL=YourOpsgenieWebhookURL
PAT=YourAzureDevOpsPersonalAccessToken
ORGANISATION=YourAzureDevOpsOrganisation
PROJECT=YourAzureDevOpsProject
TEAM=YourAzureDevOpsTeam
AREA_PATH=YourAzureDevOpsAreaPath
```
### Deploy to AWS Lambda Section


To deploy the integration as an AWS Lambda function:

1. Package your application and its dependencies.
2. Create a new Lambda function in the AWS Management Console.
3. Upload your package as the function code.
4. Set the handler to `main.lambda_handler`.
5. Configure the environment variables in the Lambda function settings to match those in your `.env` file.
6. Set up an API Gateway trigger to expose your Lambda function as an HTTP endpoint.
7. Configure Opsgenie to send alerts to the HTTP endpoint provided by API Gateway.


## Testing
The repository includes a script for running test data sets against the Lambda function. Use the `run_test_data_sets` function in `main.py` to simulate Opsgenie events and verify the integration's response.


## Usage
Once deployed, the Lambda function will automatically process incoming webhook events from Opsgenie. Ensure your Opsgenie and Azure DevOps configurations allow for the appropriate actions (create, acknowledge, close) to be performed based on the alerts.
