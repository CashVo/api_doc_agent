from agents import workflow_agent, doc_parser_agent, llm_manager
import json
from enum import Enum

class WorkflowManager:
    def __init__(self):
        self.workflow = workflow_agent.WorkflowAgent()
        self.parserAgent = doc_parser_agent.DocParserAgent()
        self.llm = llm_manager.LLMManager()

    class ACTIONS(Enum):
        '''Define a set of acceptable actions to take'''
        PARSE = "parse_content"
        NONE = "none"

    # Steps in the content curration phase
    # 1) Parse code signatures
    # 2) Add description for each class and method
    # 3) Generate class overview and introductory information
    # 4) Generate code samples for each class and method
    # 5) Generate educational content such as "how to"
    # 6) Publish API content in various formats

    def start_init_workflow(self):
        '''Build a default set of steps and start the initial workflow''' 

        step = {
            "action": self.ACTIONS.PARSE
        }
        self.workflow.add_step(step)

        self.start(self.workflow) # Start the workflow

    def start(self, workflow):
        '''Start the given workflow'''

        while (True):
            step = workflow.get_next_step()
            match step["action"]:
                case self.ACTIONS.PARSE:
                    # Call parsing agent
                    try:
                        with open('data/content_files.json', 'r') as f:
                            content_files = json.load(f)
                    except FileNotFoundError:
                        print("The file was not found.")
                    except json.JSONDecodeError:
                        print("The file is not a valid JSON.")

                    self.parserAgent.ast_parser(content_files=content_files["files"])
                case self.ACTIONS.NONE:
                    print("Nothing to do.")
                    break
                case _:
                    #Default case
                    print("* Default case")
                    break

        return True