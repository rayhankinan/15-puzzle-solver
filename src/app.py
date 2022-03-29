from flask import Flask, render_template, request, session
from puzzle import PositionMatrix, PositionTree
from dotenv import load_dotenv

import json
import os
import sys # TEMP

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/", methods = ["GET"])
def main_page():
    try:
        return render_template("index.html", matrix = PositionMatrix(json.loads(session["matrix"])))

    except KeyError:
        return render_template("index.html", matrix = PositionMatrix.getEmptyMatrix())

@app.route("/view", methods = ["GET"])
def view_page():
    try:
        PT = PositionTree(PositionMatrix(json.loads(session["matrix"])))
        pathOfStringMatrix, numOfNodes, executionTime = PT.calculate()

        return render_template("index.html", pathOfStringMatrix = pathOfStringMatrix, numOfNodes = numOfNodes, executionTime = executionTime)

    except KeyError:
        return render_template("index.html", path = [], numOfNodes = 0, executionTime = 0)

@app.route("/upload", methods = ["POST"])
def upload_txt():
    try:
        file = request.files["file"]
        session["matrix"] = json.dumps(PositionMatrix.fromFile(file.stream.read().decode("ASCII")).matrix)

        # print(PositionMatrix(json.loads(session["matrix"])).getStringMatrix(), file=sys.stdout) # REMOVE THIS

        return "Created", 201

    except Exception as e:
        return f"Bad Request: {e}", 400

@app.route("/clear", methods = ["DELETE"])
def delete_txt():
    try:
        session.pop("matrix", None)

        return "OK", 200

    except Exception as e:
        return f"Bad Request: {e}", 400

if __name__ == "__main__":
    app.run(port = 3000, debug = True)