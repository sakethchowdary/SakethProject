#! /bin/bash

echo "Building Docker Image"
sudo docker build -t backend-logic-repo:latest .
echo "Creating Tag"
sudo docker tag backend-logic-repo:latest 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest
echo "Getting Credentials"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 409043763943.dkr.ecr.us-east-1.amazonaws.com
echo "Pushing docker image to ECR"
docker push 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest
