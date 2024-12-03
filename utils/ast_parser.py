import ast, json, re
from utils import helpers, settings


class ASTParser:
    def __init__(self):
        self.packages = [] # temp storage holder
    
    def parse_file(self, content):
        '''Given the `content`, use AST to parse for class and function signatures
        Write results to file as JSON format
        '''
        self.packages = [] # Reset storage

        helpers.rich_print("Start ASTParser", "ASTPARSER:")
        # Parse the code into an AST tree
        tree = ast.parse(content)
        visitor = self._ClassVisitor(self.packages)
        visitor.visit(tree)
        return self.packages
    
    class _ClassVisitor(ast.NodeVisitor):
        def __init__(self, packages):
            self.packages = packages # Passed in by reference

        def visit_ClassDef(self, node):
            c = self._visit_ClassDef(node)
            if c is not None: 
                self.packages.append(c) 
        
        def visit_FunctionDef(self, node):
            f = self._visit_FunctionDef(node)
            if f is not None:
                self.packages.append(f) 
    
        def _visit_ClassDef(self, node):
            '''Extract all public classes and their associated public functions'''

            # Skip internal class
            if node.name.startswith('_'):
                return None

            # Extract the public class signature
            class_signature = {
                "class_name": node.name,
                "bases": [base.id for base in node.bases], # Subclass of...
                "description": "",
                "overview": "",
                "functions": []
            }

            # Extract the function signatures inside this class (include constructors and exclude private functions)
            for fn in node.body:
                results = self._visit_FunctionDef(fn)
                if results is not None:
                    class_signature['functions'].append(results)
            #storage.append(class_signature)
            return class_signature

        def _visit_FunctionDef(self, fn):
            # Ignore all inner functions within another function
            if hasattr(fn, "parent") and isinstance(fn.parent, ast.FunctionDef):
                return None

            if ( isinstance(fn, ast.FunctionDef) and ((fn.name == '__init__') or not fn.name.startswith('_')) ):
                args = {
                    "args": [*(arg.arg for arg in fn.args.args)],  # positional args
                    "varagrs": [fn.args.vararg.arg if fn.args.vararg else None],  # vararg
                    "kwargs": [fn.args.kwarg.arg if fn.args.kwarg else None],  # kwarg
                    "kwonlyargs": [*(arg.arg for arg in fn.args.kwonlyargs)]  # keyword-only args
                }
                fn_raw = ast.unparse(fn)
                fn_signature = self._parse_fn_sig(fn_raw)
                fn_info = {
                    "function_name": fn.name,
                    "args": args,
                    "signature": fn_signature,
                    "function_code": fn_raw,
                    "description": ""
                }
                #storage.append(fn_info)
                return fn_info
            else:
                return None
            
                    
        def _parse_fn_sig(self, string):
            '''Parse the function signature from a string'''

            pattern = r'def\s+(.*)\s*:' # Everything between `def` and `:` are the full function signature
            match = re.search(pattern, string)
            if match:
                return match.group(1)
            else:
                return None