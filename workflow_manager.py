from agents import doc_parser_agent, llm_manager
import json
from enum import Enum

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
parserAgent = doc_parser_agent.DocParserAgent()
llm = llm_manager.LLMManager()

class WorkflowManager:
    '''
    Manages a set of steps where each step performs a set of tasks specific for that step
    '''
    def __init__(self):
        self.workflow = self.Workflow()


    def start_init_workflow(self):
        '''Build a default set of steps and start the initial workflow''' 
        # Steps in the content curration phase (phase 1)
        # 1) Parse code signatures and output results as JSON file
        # 2) Add description for each class and method (update JSON file)
        # 3) Generate class overview and introductory information (Update JSON file)
        # 4) Generate code samples for each class and method (Update JSON file)
        # 5) Generate educational content such as "how to" topics and output as JSON file
        # 6) Publish API content in various formats

        # Defile the steps in terms of sequential tasks to accomplish
        # This is phase 1
        steps = [
            self.workflow.define_step(ACTIONS.PARSE.name, parserAgent.parse),
            # self.workflow.define_step(ACTIONS.DESCRIBE, ),
            # self.workflow.define_step(ACTIONS.OVERVIEW, ),
            # self.workflow.define_step(ACTIONS.CODE, ),
            # self.workflow.define_step(ACTIONS.EDU, ),
            # self.workflow.define_step(ACTIONS.API, ),
        ]
        self.workflow.add_steps(steps)
        self.start(self.workflow) # Start the workflow

        return llm # So we can start chatting
            # NOTE: We'll need to figure out how to hook it into the workflow

    def start(self, workflow):
        '''Start the given workflow'''

        # For phase 1: We will go through each step sequentially
        while step := workflow.get_next_step():
            step['function']() # invoke the action's function reference

        return True
    
    class Workflow:
        def __init__(self):
            self.steps = []
            self.current = -1 # starts at 0


        def define_step (self, action, function):
            '''Define a custom step or use defaults'''
            step = {
                "action": action, # Name of the task
                "function": function, # A function to execute
                #"choices": choices, # Decide which action to take from a list of choices
            }
            return step 
        
        def add_step(self, step):
            '''Add a new step to the end of the list'''
            self.steps.append(step)

        def add_steps(self, steps):
            '''Start a new workflow with the given list of steps'''
            self.steps = steps
            self.current = -1 # Reset to new workflow state

            # NOTE: May need to save the old steps in case we need to continue

        def clear_steps(self):
            '''Clear the queue'''
            self.steps = {}
            self.current = -1

        def get_next_step(self):
            '''Return the next step and advance the `current` position forward by 1'''
            if (self.current + 1) < len(self.steps):
                self.current += 1
                return self.steps[self.current]
            else:
                return self.define_step()
