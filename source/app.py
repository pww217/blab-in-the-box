from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='../templates')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        # Replace with your FastAPI server URL
        response = requests.post(
            "http://localhost:8000/api/completion", json={"input": user_input}
        )
        return jsonify(response.json())
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000)
