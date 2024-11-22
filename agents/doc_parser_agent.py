import json
from utils import ast_parser, prompt_helper 

class DocParserAgent():
    def __init__(self):
        self.documents = []
        self.ASTParser = ast_parser.ASTParser()
    
    def parse(self):
        '''Load a list of files to parse and call the parser'''

        try:
            with open('data/content_files.json', 'r') as f:
                content_files = json.load(f)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("The file is not a valid JSON.")

        self.ast_parser(content_files=content_files["files"])

    def ast_parser(self, content_files):
        '''Parse raw code file using an AST'''

        for file in content_files:
            self.documents.append(self.ASTParser.parse_file(file=file))
        return self.documents
    

    # WARNING: Currently not working as expected as the `prompt_template` being too large when the full code is added
    # LLM takes too long to parse and response. May want to chunk it up
    def llm_parser(self, content_files, llm):
        '''Parse raw code file using an LLM'''

        prompt_text = prompt_helper.PARSER_TEXT

        # Load raw code content
        for file in content_files:
            with open(file, 'r') as f:
                content = f.read()
            self.documents.append(content)
        
        # Query LLM to help parse raw code file into a JSON format
        prompt_template = f'''Parse the following RAW CODE for class and their function signatures. Return results as a JSON object.
        ADDITIONAL INSTRUCTIONS:
        - Parse for public classes and functions only
        - Ignore all internal classes and functions (e.g.: anything starting with `_` in the name indicates internal or private)
        - Return results as a JSON object and nothing else
        - Use a JSON FORMAT as described below.
        {prompt_text.JSON_FORMAT.value}

        EXAMPLES: 
        {prompt_text.EXAMPLES.value}

        
        Context
        RAW CODE: 
        {self.documents}
        '''
        response = llm.prompt(prompt_template)
        return response.response

