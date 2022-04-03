from flask import Flask, render_template, request, session, jsonify
from puzzle import PositionMatrix, PositionTree
from pyfladesk import init_gui

import json
import secrets
import os
import numpy as np

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

@app.route("/upload_txt", methods = ["POST"])
def upload_txt():
    try:
        file = request.files["file"]
        session["matrix"] = json.dumps(PositionMatrix.fromFile(file.stream.read().decode("ASCII")).matrix.tolist())

        return "Created", 201

    except Exception as e:
        session["matrix"] = json.dumps(PositionTree.targetPosition.matrix.tolist())

        return str(e), 400

@app.route("/calculate", methods = ["GET"])
def calculate_matrix():
    try:
        PT = PositionTree(PositionMatrix(np.array(json.loads(session["matrix"]))))
        sumKurangPlusX, pathOfMatrix, numOfNodes, executionTime = PT.calculate()

        return jsonify(sumKurangPlusX = sumKurangPlusX, pathOfMatrix = pathOfMatrix, numOfNodes = numOfNodes, executionTime = executionTime, nRow = PositionMatrix.nRow, nCol = PositionMatrix.nCol)

    except KeyError:
        return "Please upload a txt file first!", 400

@app.route("/upload_json", methods = ["POST"])
def process_matrix():
    try:
        data = request.get_json()
        session["matrix"] = json.dumps(data)

        return "Created", 201

    except Exception as e:
        session["matrix"] = json.dumps(PositionTree.targetPosition.matrix.tolist())

        return str(e), 400

if __name__ == "__main__":
    icondir = os.path.join(os.path.dirname(__file__), "static/images/logo.png")

    init_gui(app, port = 3000, window_title = "15 Puzzle Solver", icon = icondir)