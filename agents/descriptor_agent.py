from agents.llm_manager import LLMManager
from agents.base_agent import BaseAgent
from utils.workflow import Workflow
from utils import helpers, settings, prompt_helper
from tqdm import tqdm
import time, json
#from rich import console

class DescriptorAgent(BaseAgent):
    '''An agent that can help provide short descriptions'''
    def __init__(self, llm: LLMManager):
        super().__init__(llm)
        self.workflow = Workflow()
        self.PROMPT_TEMPLATES = prompt_helper.PROMPT_TEMPLATES()


    def generate_descriptions(self, package_content):
        '''
        Load the "ast_output.json file and generate description for each parts of the doc
        '''

        # Build the steps for each description task
        steps = [] 
        for p in package_content: # e.g.: p = "{ class_name: '...'}" or "{ function_name: '...'}"
            # Handle case: class description
            if "class_name" in p: 
                steps.append(self.workflow.create_step(
                        "CLASS:"+p['class_name'], 
                        self.get_description, 
                        content = [f['function_name'] for f in p['functions']], objref = p, objtype="class", objname=p['class_name']
                    )
                )

                # Handle case: function description for each functions within the class
                for fn in p['functions']:
                    steps.append(self.workflow.create_step(
                            "FUNCTION:"+fn['function_name'], 
                            self.get_description,
                            content = fn['signature'], objref = fn, objtype='function', objname=fn['function_name']
                        )
                    )

                    # Handle case: args description for each arguments within the function
                    for a in fn["args"]:
                            steps.append(self.workflow.create_step(
                                    "FUNCTIONARGS:"+fn['function_name'], 
                                    self.get_description,
                                    content = a, objref = a, objtype='parameter', objname=a['arg_name']
                                )
                            )

            # Handle package functions not inside a class
            elif "function_name" in p:
                steps.append(self.workflow.create_step(
                        "FUNCTION:"+p['function_name'], 
                        self.get_description,
                        content = p['signature'], objref = p, objtype='function', objname=p['function_name']
                    )
                )

                # Handle case: args description for each arguments within the function
                for a in p["args"]:
                    steps.append(self.workflow.create_step(
                            "FUNCTIONARGS:"+p['function_name'], 
                            self.get_description,
                            content = a, objref = a, objtype='parameter', objname=a['arg_name']
                        )
                    )

        self.workflow.add_steps(steps)

        pbar = tqdm(total=len(steps), desc="Workflow Progress", unit="Step", colour="green")
        # Execute workflow
        while (step := self.workflow.get_next_step()) is not None:
            pbar.update(1)
            step['call_function'](*step['args'], **step['kwargs']) # Execute the func in the step

        pbar.close()
        return True
            
    def get_description(self, content, objref, objtype, objname):
        helpers.rich_print(f'\nGenerating description for [yellow]{objtype}: {objname}[/yellow]')

        template_name = "GENERATE_DESCRIPTION" # if objtype == "parameter" else "GENERATE_DESCRIPTION"
        prompt_template = self.PROMPT_TEMPLATES.get_template(template_name, objtype=objtype, objname=objname, content=content)
        helpers.rich_print(f"\n{prompt_template}\n","[orange]Prompt Template[/orange]") # debugging
        
        with helpers.console.status("LLM thinking...", spinner="dots"):
            if objname == "NoArgs":
                results['response'] = '[{"arg": "None"}]'
                helpers.rich_print("Ignored LLM prompting. Parameter list is empty", 'note')
            else:
                results = self.llm.prompt(prompt_template)
        
        objref['description'] = results['response'] # Save the description back into the referenced object
        helpers.print_log(f"'{objtype} {objname}' description: \n[blue]{results['response']}[/blue]")
        return results['response']
    