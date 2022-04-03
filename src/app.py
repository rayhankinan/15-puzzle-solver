from flask import Flask, render_template, request, session, jsonify
from puzzle import PositionMatrix, PositionTree

import json
import secrets
import numpy as np
import sys # HILANGKAN IMPORT SYS KETIKA DIKUMPULKAN

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_urlsafe()

# FRONTEND
@app.route("/", methods = ["GET"])
def main_page():
    return render_template("index.html")

@app.route("/view", methods = ["GET"])
def view_page():
    return render_template("view.html")

# BACKEND
@app.route("/display", methods = ["GET"])
def display_matrix():
    try:
        return jsonify(matrix = PositionMatrix(np.array(json.loads(session["matrix"]))).matrix.tolist(), nRow = PositionMatrix.nRow, nCol = PositionMatrix.nCol)

    except KeyError:
        return jsonify(matrix = PositionTree.targetPosition.matrix.tolist(), nRow = PositionMatrix.nRow, nCol = PositionMatrix.nCol)

@app.route("/calculate",  methods = ["GET"])
def calculate_matrix():
    try:
        PT = PositionTree(PositionMatrix(np.array(json.loads(session["matrix"]))))
        sumKurangPlusX, pathOfMatrixNP, numOfNodes, executionTime = PT.calculate()

        return jsonify(sumKurangPlusX = sumKurangPlusX, pathOfMatrix = pathOfMatrixNP.tolist(), numOfNodes = numOfNodes, executionTime = executionTime, nRow = PositionMatrix.nRow, nCol = PositionMatrix.nCol)

    except:
        return jsonify(sumKurangPlusX = 0, pathOfStringMatrix = [], numOfNodes = 0, executionTime = 0, nRow = PositionMatrix.nRow, nCol = PositionMatrix.nCol)

@app.route("/upload", methods = ["POST"])
def upload_txt():
    try:
        file = request.files["file"]
        session["matrix"] = json.dumps(PositionMatrix.fromFile(file.stream.read().decode("ASCII")).matrix.tolist())

        print(PositionMatrix(np.array(json.loads(session["matrix"]))).matrix, file=sys.stdout) # REMOVE THIS

        return "Created", 201

    except Exception as e:
        session.pop("matrix", None)

        return str(e), 400

@app.route("/clear", methods = ["DELETE"])
def delete_txt():
    try:
        session.pop("matrix", None)

        return "OK", 200

    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(port = 3000, debug = True) # HILANGKAN DEBUG KETIKA DIKUMPULKAN