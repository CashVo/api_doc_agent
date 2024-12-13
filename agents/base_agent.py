from agents.llm_manager import LLMManager
from agents.grader_agent import GraderAgent
from agents.editor_agent import EditorAgent
from utils import helpers

class BaseAgent:
    def __init__(self, llm: LLMManager):
        self.llm = llm
        self.functions = {} # function calling tools
        self.grader = GraderAgent(llm)
        self.editor = EditorAgent(llm)

    def add_function(self, func_name, func):
        '''Add a list of tools as an array of function names
        @Params
        func_name: The function's name (e.g.: "Add")
        func: The function to call (e.g.: calculator.add)
        '''
        self.functions[func_name] = func

    def call_function(self, func_name, *args):
        result = self.functions[func_name](args)
        return result
    
    def grade_and_edit(self, objref, **kwargs):
        helpers.print_log(f"\nOriginal description: {kwargs['content']}", "GRADE+EDIT")
        results = self.grader.grade_this(**kwargs)
        objref['grade'] = results['response'] # Save the grade and suggestions
        helpers.print_log(results['response'], '[green]GRADE RESPONSES[/green]\n')
        if "GREAT" not in results['response']:
            results = self.editor.edit_this(suggestions=results['response'], **kwargs)
            helpers.print_log("", '[green]EDITING COMPLETE![/green]\n')
        else:
            helpers.print_log("Grade was [GREAT]! No edits needed.", '[green]GRADE RESPONSES[/green]\n')
            results['response'] = kwargs['content'] # Give the original content back
        return results
