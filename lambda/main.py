import json
import boto3
from os import environ

def stopTasks(ID, KEY):
    clusterName = environ.get("CLUSTER")
    client = boto3.client(
        "ecs",
        aws_access_key_id = ID,
        aws_secret_access_key = KEY
    )
    response = client.list_tasks(cluster=clusterName)
    tasks = response["taskArns"]
    for task in tasks:
        response = client.stop_task(
            cluster=clusterName,
            task=task,
            reason='Desired count changed'
        )
    changeCount(0, ID, KEY)

def changeCount(desiredCount, ID, KEY):
    clusterName = environ.get("CLUSTER")
    client = boto3.client(
        "ecs",
        aws_access_key_id = ID,
        aws_secret_access_key = KEY
    )
    print("client created")
    # List all running services
    try:
        response = client.list_services(cluster=clusterName)
    except Exception as e:
        print("error found", e)
    # Get ARN of the service
    arn = response["serviceArns"][0]
    # Update service desiredCoount
    response = client.update_service(
        cluster = clusterName,
        service = arn,
        desiredCount = desiredCount
    )
    print(f"Updated desiredCount to {desiredCount}")
    

def lambda_handler(event, context):
    # Gather data from env
    ID = environ.get("ID")
    print(ID)
    KEY = environ.get("KEY")
    if event["operation"] == "updateCount":
        print("Updating count of tasks")
        changeCount(event["count"], ID, KEY)
    elif event["operation"] == "stopTasks":
        stopTasks(ID, KEY)
