# PROJECT
Idea is to create a python based machine learning application container and deploy to AWS ECS with autoscaling and load balancing enabled. An application load balancer will be used to face the incoming traffic and serve the data through the same.

## Docker commands
`docker build -t saketh .`
`docker run -d --name saketh -p 3000:3000 saketh`

## Running python flask in bg
`nohup python3 app.py &`
