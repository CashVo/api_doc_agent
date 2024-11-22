# Change Log

## 11/21/24: Code Refactoring - focused on workflow setup
* Refactor how `workflow_manager` work. Moved `workflow_agent` into this class an removed the `workflow_agent` file
  * For phase 1, not much user interaction and the WorkflowManager just builds a set of steps and execute one in order
  * As we go through the steps, we will need to figure out how to pause the step and take user input and then continue with that step...hopefully this will become more clear as we build out the work for subsequent steps.
* Break the change log out into it's own file (this one) so we don't over crowd README
* Add a workflow diagram for phase 1 in the README

## 11/20/24: Added Workflow and Parsing agents
* Workflow Agent: Got a basic workflow manager setup to handle the content parsing step
* Parsing Agent:  
  * I got two parsing functions defined. One using AST and the other using LLM.
  * At first, I thought I could pass in the entire code file along with prompt template to get the LLM to do all the parsing and writing in one go. But, it's taking way too long to response. Longest wait time was about 3hrs and not even returning with a response. So, I am not sure what it was able to generate in that run. It would save us a lot of coding if I have more powerful hardware to let the LLM do most of the work.
  * So, the fallback plan is manually parse the code file for class and function signatures. Then, iteratively prompt the LLM to provide the descriptions
