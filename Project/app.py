from flask import jsonify, Flask, render_template, request
from main import operation1
import json

app = Flask(__name__)

@app.route("/")
def Hello():
    return "<p>Hello World!</p>"

@app.route("/getdata", methods=['POST', 'GET'])
def performOperation1():
    if request.method == "POST":
        history = int(request.args.get("history"))
        shots = int(request.args.get("shots"))
        x, y =operation1(history, shots)
        return (jsonify([x, y]), history, shots)
    else:
        x, y = operation1(100, 10000)
        return (jsonify([x, y], 100, 10000), str(100), str(10000))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3002)
