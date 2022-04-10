from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def HelloWorld():
    return "Hello World!"

@app.route("/manage", methods=["GET"])
def printData():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    url = "http://EC2Co-EcsEl-10BCU9C7X6FZN-1450603549.us-east-1.elb.amazonaws.com:3000/getdata"
    print(url)
    response = requests.get(
        url = url,
        headers=headers
    )
    data = response.json()
    return render_template("allData.html", data=data[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3001)
