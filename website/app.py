from flask import Flask, jsonify, render_template, request
import requests
import boto3, json
from time import sleep

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def HelloWorld():
    return "Hello World!"

@app.route("/default", methods=["GET"])
def defGraph():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    url = "http://EC2Co-EcsEl-10BCU9C7X6FZN-1450603549.us-east-1.elb.amazonaws.com:3000/getdata"
    print(url)
    try:
        response = requests.get(
            url = url,
            headers=headers
        )
        data = response.json()
        print(data)
        labels = [list(key.keys())[0] for key in data]
        # print(labels)
        v1 = [datum.get(list(datum.keys())[0]) for datum in data]
        values = [[row[1] for row in v1], [row[2] for row in v1], [row[3] for row in v1]]
        # print(values)
        return render_template("defaultGraph.html", data=data[0], labels=labels, values=values)
    except Exception as e:
        return render_template("error.html", message="Error calling ECS API. please check tasks in AWS.")

@app.route("/", methods=["GET"])
def printData():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    url = "http://EC2Co-EcsEl-10BCU9C7X6FZN-1450603549.us-east-1.elb.amazonaws.com:3000/getdata"
    print(url)
    try:
        response = requests.get(
            url = url,
            headers=headers
        )
        data = response.json()
        return render_template("allData.html", data=data[0])
    except Exception as e:
        return render_template("error.html", message="Error calling ECS API. please check tasks in AWS.")

@app.route("/settings", methods=["GET", "POST"])
def updateTasksDef():
    if request.method == "POST":
        print("POST CALLED")
        req_arn, tasks_count = taskInformation()

        # Fetch data from payload
        data = request.form['count']
        if data == 0:
            response = updateTaskInformation(
                payload=json.loads('{"operation": "stopTasks"}')
            )
            print(response)
            sleep(3)
            return render_template("settings.html", 
                arn=req_arn, 
                count=tasks_count,
                message="Updated... please refresh page after few seconds."
            )
        else:
            print(f"Updating to {data} tasks")
            # Update task definition
            response = updateTaskInformation(
                payload=json.loads('{"operation": "updateCount","count": ' + str(data) + '}')
                )
            print(response)
            sleep(3)
            return render_template("settings.html", 
                arn=req_arn, 
                count=tasks_count,
                message="Updated... please refresh page after few seconds."
            )

    elif request.method == "GET":
        print("GET CALLED")
        req_arn, tasks_count = taskInformation()
        return render_template("settings.html", arn=req_arn, count=tasks_count, message="")


def taskInformation():
    # Get current status from ECS
    ID = "AKIAV6PHIQLTUBMHJTE6"
    KEY = "f+jTGcl0TpTkeJ3TTDZ3LdSwERAf4WjzoDa1D+Jy"
    client = boto3.client(
        'ecs',
        aws_access_key_id=ID,
        aws_secret_access_key=KEY
    )
    response = client.list_clusters(maxResults=2)
    req_arn = response['clusterArns'][0]
    response = client.list_tasks(cluster=req_arn)
    tasks_count = len(response['taskArns'])
    return req_arn, tasks_count

def updateTaskInformation(payload):
    ID = "AKIAV6PHIQLTUBMHJTE6"
    KEY = "f+jTGcl0TpTkeJ3TTDZ3LdSwERAf4WjzoDa1D+Jy"
    client = boto3.client('lambda',aws_access_key_id=ID,aws_secret_access_key=KEY)

    # Payload
    print(payload)
    response = client.invoke(
        FunctionName='manageECS',
        # InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3001)
