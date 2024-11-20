from utils import ast_parser, prompt_helper 


class DocParserAgent():
    def __init__(self):
        self.documents = []
        self.ASTParser = ast_parser.ASTParser()

    def ast_parser(self, content_files):
        '''Parse raw code file using an AST'''

        for file in content_files:
            self.documents.append(self.ASTParser.parse_file(file=file))
        return self.documents
    
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

