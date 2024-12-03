from flask import Flask, render_template, request
from utils import  helpers, workflow
from agents.llm_manager import LLMManager
from agents.doc_parser_agent import DocParserAgent
from agents.descriptor_agent import DescriptorAgent
import content_curration_workflow

app = Flask(__name__)

AIAssistant = LLMManager()
# Agents
agents = {
    "parserAgent": DocParserAgent(),
    'descriptorAgent': DescriptorAgent(AIAssistant)
}

helpers.rich_print("\nMulti-ReAct agent initializing!!! \n", "APP:")


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
    content_curration_workflow.start_curration_workflow(agents)
    app.run(debug=True)
