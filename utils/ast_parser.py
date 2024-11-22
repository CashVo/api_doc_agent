import ast, json, re

class ASTParser:
    def __init__(self):
        self.classes = []

    
    def parse_file(self, file):
        '''Parse a code file into an AST'''

        # Parse the code into an AST tree
        with open(file, 'r') as f:
            tree = ast.parse(f.read())

        # Walk the tree and parse the classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._visit_ClassDef(node=node)

        # Print the class signatures
        results = json.dumps(self.classes, indent=4) # Convert the json object to string
        print(results)

        with open('data/processed/ast_output.json', 'w') as f:
            f.write(results)

        return self.classes
    
    def _visit_ClassDef(self, node):
        '''Extract all public classes and their associated public functions'''

        # Skip internal class
        if node.name.startswith('_'):
            return

        # Extract the public class signature
        class_signature = {
            "name": node.name,
            "bases": [base.id for base in node.bases], # Subclass of...
            "functions": []
        }

        # Extract the function signatures inside this class (include constructors and exclude private functions)
        for fn in node.body:
            if ( isinstance(fn, ast.FunctionDef) and ((fn.name == '__init__') or not fn.name.startswith('_')) ):
                args = {
                    "args": [*(arg.arg for arg in fn.args.args)],  # positional args
                    "varagrs": [fn.args.vararg.arg if fn.args.vararg else None],  # vararg
                    "kwargs": [fn.args.kwarg.arg if fn.args.kwarg else None],  # kwarg
                    "kwonlyargs": [*(arg.arg for arg in fn.args.kwonlyargs)]  # keyword-only args
                }
                fn_signature = self._parse_fn_sig(ast.unparse(fn))
                class_signature['functions'].append({
                    "name": fn.name,
                    "args": args,
                    "signature": fn_signature
                })
            
        self.classes.append(class_signature)

    def _parse_fn_sig(self, string):
        '''Parse the function signature from a string'''

        pattern = r'def\s+(.*)\s*:' # Everything between `def` and `:` are the full function signature
        match = re.search(pattern, string)
        if match:
            return match.group(1)
        else:
            return None