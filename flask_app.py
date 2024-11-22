from flask import Flask, render_template, request
from utils import  helpers
from workflow_manager import WorkflowManager

app = Flask(__name__)

WorkflowManager = WorkflowManager()
AIAssistant = WorkflowManager.start_init_workflow()

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
    response = AIAssistant.prompt(user_input)

    html_response = f"{response}"

    return { "response": html_response }, 200

if __name__ == "__main__":
   app.run(debug=True)
