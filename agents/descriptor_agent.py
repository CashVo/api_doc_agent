from agents.llm_manager import LLMManager
from agents.base_agent import BaseAgent
from utils.workflow import Workflow
from utils import helpers, settings
from tqdm import tqdm
import time, json
#from rich import console

class DescriptorAgent(BaseAgent):
    '''An agent that can help provide short descriptions'''
    def __init__(self, llm: LLMManager):
        super().__init__(llm)
        self.workflow = Workflow()


    def generate_descriptions(self, package_content):
        '''
        Load the "ast_output.json file and generate description for each parts of the doc
        '''

        # Build the steps for each description task
        steps = [] 
        for pkg_name, pkgs in package_content.items(): # e.g:  pkg = "collection.py", pkgs = {...}
            for p in pkgs: # e.g.: p = "{ class_name: '...'}" or "{ function_name: '...'}"
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
                                content = fn['function_code'], objref = fn, objtype='function', objname=fn['function_name']
                            )
                        )

                        # Handle case: args description for each arguments within the function
                        steps.append(self.workflow.create_step(
                                "FUNCTIONARGS:"+fn['function_name'], 
                                self.get_args_description,
                                content = fn['signature'], objref = fn, objtype='parameter', objname=fn['function_name'], clsname=p['class_name']
                            )
                        )

                # Handle package functions not inside a class
                elif "function_name" in p:
                    steps.append(self.workflow.create_step(
                            "FUNCTION:"+p['function_name'], 
                            self.get_description,
                            content = p['function_code'], objref = p, objtype='function', objname=p['function_name']
                        )
                    )

                    # Handle case: args description for each arguments within the function
                    steps.append(self.workflow.create_step(
                            "FUNCTIONARGS:"+p['function_name'], 
                            self.get_args_description,
                            content = p['signature'], objref = p, objtype='parameter', objname=p['function_name'], clsname=""
                        )
                    )


            


        # for cls in code_classes:
        #     # Steps to generate class descriptions
        #     steps.append(self.workflow.create_step(
        #                 "CLASS:"+cls['class_name'], 
        #                 self.get_description, 
        #                 content = cls, objtype="class", objname=cls['class_name']
        #             )
        #         )

        #     # Steps to generate function descriptions
        #     for fn in cls['functions']:
        #         steps.append(self.workflow.create_step(
        #                 "FUNCTION:"+fn['function_name'], 
        #                 self.get_description,
        #                 content = fn, objtype='function', objname=fn['function_name']
        #             )
        #         )
        #         # Step to generate descriptions for each parameters
        #         steps.append(self.workflow.create_step(
        #                 "FUNCTIONARGS:"+fn['function_name'], 
        #                 self.get_args_description,
        #                 content = fn['signature'], objtype='parameter', objname=fn['function_name'], clsname=cls['class_name']
        #             )
        #         )


        self.workflow.add_steps(steps)

        pbar = tqdm(total=len(steps), desc="Workflow Progress", unit="Step", colour="green")
        tStart = time.time()
        # Execute workflow
        while (step := self.workflow.get_next_step()) is not None:
            pbar.update(1)
            step['call_function'](*step['args'], **step['kwargs']) # Execute the func in the step

        pbar.close()
        elapsed_time = (tStart - time.time()) / 60 # Convert to minutes
        helpers.print_log(f"Total elapsed time (GenDescription Workflow): {elapsed_time} min")
        return True
            
    def get_description(self, content, objref, objtype, objname):
        helpers.rich_print(f'\nGenerating description for [yellow]{objtype}: {objname}[/yellow]')

        prompt_template = f'''
        As a PyTorch expert developer, describe the purpose and functionality of the {objtype}: `{objname}`
        Explain its significance and how it should be used.
        - return a concise description only.
        - start the description with: "This {objtype} is "
        
        Here is the {objtype} details:
        {content}
        '''
        with helpers.console.status("LLM thinking...", spinner="dots"):
            results = self.llm.prompt(prompt_template)
        
        objref['description'] = results['response'] # Save the description back into the referenced object
        helpers.print_log(f"{objtype} {objname} description: \n[blue]{results['response']}[/blue]")
        return results['response']
    
    def get_args_description(self, content, objref, objtype, objname, clsname):
        helpers.rich_print(f'\nGenerating [yellow]Args description:[/yellow]')

        param_format = '''        
        [{
            "arg": "<parameter name>"
            "description": " (<type>) - <description and purpose>. (default: <default value, if any, otherwise say None>)"
        }]        
        '''

        examples = '''
        EXAMPLES:
        - signature: "load_state_dict(self, state_dict: OrderedDict) -> None"
          output:
            [
                {
                    "arg": "state_dict",
                    "description": "(OrderedDict) - The model state dictionary to be loaded into the current state."       
                }
            ]
        
        - signature: "set_seed(self, seed: int, static_seed: bool=False) -> int"
          output:
            [  
                {
                    "arg": "seed",
                    "description": " (int) - The random seed to be used. (default: None)"
                },
                {
                    "arg": "static_seed",
                    "description": " (bool) - Whether the static seed is used. (default: False)"
                }
            ]
        '''

        prompt_template = f'''
        As a PyTorch expert developer, describe each {objtype} of the function {objname}.

        INSTRUCTIONS
        - Ignore the following parameters: [self | args | kwargs]
        - Return the response as defined by the output format below. 
        OUTPUT FORMAT - Folow this format exactly -- Do not deviate -- Do not explain yourself!
          {param_format}
        
        CONTEXT: here is the full function signature
        {content}

        {examples}
        '''

        helpers.rich_print(f'RAW Signature: \n====\n{repr(content)}\n====\n')

        retries = 3
        results = {}
        while retries > 0:
            try:
                # Show status spinner while LLM processes the prompt
                with helpers.console.status("LLM thinking...", spinner="dots9"):
                    if helpers.ignore_args_check(content) is False:
                        results = self.llm.prompt(prompt_template)
                    else:
                        results['response'] = '[{"arg": "None"}]'
                        helpers.rich_print("Ignored LLM prompting. Parameter list is empty", 'note')
                
                # Attempt to parse the response JSON
                json_args = json.loads(results['response'].strip())
                objref['args'] = json_args

                # Log and return the parsed JSON
                helpers.print_json(json_args, log=True)
                return json_args

            except json.JSONDecodeError as e:
                retries -= 1
                helpers.rich_print(
                    f"Attempt failed with JSONDecodeError: {e}\nRetries left: {retries}",
                    "error"
                )
                helpers.rich_print(repr(results['response']))
                if retries == 0:
                    raise Exception("Failed to parse LLM response after multiple attempts.") from e
            except Exception as e:
                # Catch-all for unexpected errors
                helpers.rich_print(f"Unexpected error: {e}", "Error")
                raise  # Re-raise to ensure the program doesn't proceed in an unstable state
    

