# PROJECT
Idea is to create a python based machine learning application container and deploy to AWS ECS with autoscaling and load balancing enabled. An application load balancer will be used to face the incoming traffic and serve the data through the same.

## SSH 
`ssh -i AWS/BackendLogic-KP.pem ec2-user@44.202.146.244`

## Docker commands
`aws configure` (entries in AWS/new_user_credentials file)

`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 409043763943.dkr.ecr.us-east-1.amazonaws.com`

`docker build -t backend-logic-repo:latest .` (Being in Project folder in EC2)

`docker tag backend-logic-repo:latest 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest`

`docker push 409043763943.dkr.ecr.us-east-1.amazonaws.com/backend-logic-repo:latest`

## URLs and other Information
Loadbalancer URL : http://ec2co-ecsel-10bcu9c7x6fzn-1450603549.us-east-1.elb.amazonaws.com:3000/getdata

## TODO
- Completely watch https://www.youtube.com/watch?v=dam0GPOAvVI
- Host flask application in GCP
https://www.youtube.com/watch?v=_OqxXjiASDI