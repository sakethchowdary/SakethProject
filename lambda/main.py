import json
import boto3

def stopTasks():
    clusterName = "backend-logic-fargate-cluster"
    client = boto3.client(
        "ecs"
    )
    response = client.list_tasks(cluster=clusterName)
    tasks = response["taskArns"]
    for task in tasks:
        response = client.stop_task(
            cluster=clusterName,
            task=task,
            reason='Desired count changed'
        )
    changeCount(0)

def changeCount(desiredCount):
    clusterName = "backend-logic-fargate-cluster"
    client = boto3.client(
        "ecs",
        aws_access_key_id = "AKIAV6PHIQLTWMQBJNTQ",
        aws_secret_access_key = "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"
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
    print(event)
    if event["operation"] == "updateCount":
        print("Updating count of tasks")
        changeCount(event["count"])
    elif event["operation"] == "stopTasks":
        stopTasks()
