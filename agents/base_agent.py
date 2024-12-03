from agents.llm_manager import LLMManager

class BaseAgent:
    def __init__(self, llm: LLMManager):
        self.llm = llm
        self.functions = {}

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