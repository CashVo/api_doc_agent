from flask import Flask, render_template, request
import ollama
from utils.helpers import *

app = Flask(__name__)

print("ReAct agent initialized!!! Reay to chat...")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    print("Start chatting...")
    user_input = request.json.get("user_input")
    if not user_input:
        return {"error": "Prompt is required"}, 400

    # Generate response 
    response = basic_prompt(user_input)

    html_response = f"{response}"

    return { "response": html_response }, 200

if __name__ == "__main__":
   app.run(debug=True)
