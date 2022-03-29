from flask import Flask, render_template, request, session
from puzzle import PositionMatrix, branchAndBound

import sys # TEMP

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_txt():
    try:
        file = request.files["file"]
        session["matrix"] = PositionMatrix(file.stream.read().decode("ASCII"))

        return "Created", 201

    except Exception as e:
        return f"Bad Request: {e}", 400

@app.route("/clear", methods=["DELETE"])
def delete_txt():
    try:
        session.pop("matrix", None)

        return "OK", 200

    except Exception as e:
        return f"Bad Request: {e}", 400

if __name__ == "__main__":
    app.run(port=3000, debug=True)