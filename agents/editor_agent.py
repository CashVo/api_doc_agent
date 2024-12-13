from agents.llm_manager import LLMManager
from utils.workflow import Workflow
from utils import helpers, settings, prompt_helper
from tqdm import tqdm
import time, json
#from rich import console

class EditorAgent():
    '''An agent that can help grade the content, give a grade, and provide improvement suggestions'''
    def __init__(self, llm: LLMManager):
        self.llm = llm
        self.workflow = Workflow()
        self.PROMPT_TEMPLATES = prompt_helper.PROMPT_TEMPLATES()


    def edit_this(self, **kwargs):
        prompt_template = self.PROMPT_TEMPLATES.get_template("EDITOR", **kwargs)
        helpers.rich_print(f"{prompt_template}","\n\n[magenta on yellow] EDITOR Prompt Template [/magenta on yellow]") # debugging
        return self.llm.prompt(prompt_template)