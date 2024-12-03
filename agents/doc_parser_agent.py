from utils import ast_parser, helpers, settings

class DocParserAgent():
    def __init__(self):
        self.documents = []
        self.ASTParser = ast_parser.ASTParser()
    
    def parse(self, content):
        '''Load a list of files to parse and call the parser'''
        helpers.rich_print("Start parsing code...", "PARSER:")

        results = self.ASTParser.parse_file(content) # Parse using an AST library

        helpers.rich_print(f'Finished parsing code.', "PARSER:")

        return results
