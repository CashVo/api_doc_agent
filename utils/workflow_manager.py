import json
from enum import Enum
from agents import llm_manager, doc_parser_agent, descriptor_agent
from utils import workflow

class ACTIONS(Enum):
    '''Define a set of acceptable actions to take'''
    PARSE = "Parse raw code file"
    DESCRIBE = "Generate a description"
    OVERVIEW = "Generate overview and introduction"
    CODE = "Generate working code samples and snippets"
    EDU = "Generate help articles and useful user guides"
    API = "Generate final API content"
    NONE = "none"
    DONE = "done"
    DEVMGR = "Run Dev Manager"
ACTIONS = ACTIONS # Create an instant so the classes below can use it

# Agents
llm = llm_manager.LLMManager()
parserAgent = doc_parser_agent.DocParserAgent()
descriptorAgent = descriptor_agent.DescriptorAgent(llm)

class WorkflowManager:
    '''
    Manages a set of steps where each step performs a set of tasks specific for that step
    '''
    def __init__(self):
        self.workflow = workflow.Workflow()
    
    def create_workflow(self):
        '''Create a new workflow and return an instance of that object'''
        return workflow.Workflow()

    def start_workflow(self, workflow, *args):
        '''Start the given workflow'''

        # For phase 1: We will go through each step sequentially
        while step := workflow.get_next_step():
            if step is not None:
                step['function'](args) # invoke the action's function reference

        return True
    
    