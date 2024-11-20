# API Doc Agent Project
This project implements an end2end experience for an API content writer. It consists of two primiary aspects:
1. The content currating process. This is where we take the raw code representing the public API and ask LLM to help us write the user docs.
2. The content serving process. This is where end users can interact with a Chat Agent via a GUI to learn about the API and how to use it in their own projects.

## Workflow Diagram - Overview
The conceptual overview of what this project aims to accomplish is as follows.
![Overview diagram](utils/assets/e2e%20Doc%20Agent%20workflow.png)

## Currating Features
These are some key features relating to the curration process
* Specialized agents working together with orchastrating agents to produce API docs ... with user-in-the-loop to verify quality and completeness
* This agent is fine-tuned for Python code projects
* Produce final SDK content in various formats (e.g.: MD, HTML, JSON, XML)

## Chat Serving Features
These are some key features relating to the serving of content process.
* Content is stored in a vector index for semantic search couple with LLM for NLP
* Users can chat with the content through an assistant (via a GUI)
* Agent will apply reasoning over the response before providing user with final response


## Setup
1. Install Python (latest)
1. Pip install all requirements: `pip install -r requirements.txt`
1. Create a new virtual environemnt: `python -m venv venv`
1. Activate the virtual environment: `venv/Scripts/activate`
1. Run the Flask agent: `python flask_app.py`...follow instructions in terminal to find the web endpoint for the Agent's Web UI. Start chatting with the Doc Bot Agent from there.

## Remarks
* 


# Change Log

## 11/20/24: Added Workflow and Parsing agents
* Workflow Agent: Got a basic workflow manager setup to handle the content parsing step
* Parsing Agent:  
  * I got two parsing functions defined. One using AST and the other using LLM.
  * At first, I thought I could pass in the entire code file along with prompt template to get the LLM to do all the parsing and writing in one go. But, it's taking way too long to response. Longest wait time was about 3hrs and not even returning with a response. So, I am not sure what it was able to generate in that run. It would save us a lot of coding if I have more powerful hardware to let the LLM do most of the work.
  * So, the fallback plan is manually parse the code file for class and function signatures. Then, iteratively prompt the LLM to provide the descriptions
