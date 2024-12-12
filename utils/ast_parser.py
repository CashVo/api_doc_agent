import ast, json, re
from utils import helpers, settings
from typing import List, Dict


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
                "docstring": self._get_docstring(node),
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
                fn_raw = ast.unparse(fn)
                fn_signature = self._parse_fn_sig(fn_raw)
                args = self._parse_args_signature(fn_signature)
                

                fn_info = {
                    "function_name": fn.name,
                    "args": args,
                    "signature": fn_signature,
                    "function_code": fn_raw,
                    "docstring": self._get_docstring(fn),
                    "description": ""
                }
                #storage.append(fn_info)
                return fn_info
            else:
                return None
            
        def _get_docstring(self, node):
            '''Return the docstring or an empty string'''
            ds = ast.get_docstring(node)
            return ds if ds is not None else ""
        
        def _parse_fn_sig(self, string):
            '''Parse the function signature from a string'''

            pattern = r'def\s+(.*)\s*:' # Everything between `def` and `:` are the full function signature
            match = re.search(pattern, string)
            if match:
                return match.group(1)
            else:
                return None
            
        def _parse_args_signature(self, signature: str) -> List[Dict[str, str]]:
            # Remove the function name and opening parenthesis
            args_section = signature.split("(", 1)[1].rsplit(")", 1)[0]

            if "__init__" in signature:
                pass

            # Regex to capture arguments in the format:
            # arg_name: type_hint=default_value
            arg_pattern = re.compile(
                r"""
                (?P<arg_name>[\w*]+)             # Argument name, including '*' or '**'
                (?:\s*:\s*(?P<return_type>(?:[^\[,=])*(?:(\[([^:])*\])*)(?:[^=,]*)))?  # Optional type hint
                (?:\s*=\s*(?P<default_value>[^,]+))? # Optional default value
                """,
                re.VERBOSE,
            )

            # (?:\s*:\s*(?P<return_type>[^\[,]+(?:(\[([^\]]|[\]])*\])*)(?:[^=,]*)))

            # Parse arguments
            args = []
            ignored_set = set(["self", "*", "*args", "**kwargs"]) # Drop these args from the list
            for match in arg_pattern.finditer(args_section):
                arg = {
                    "arg_name": match.group("arg_name").strip(),
                    "return_type": (match.group("return_type") or "").strip(),
                    "default_value": (match.group("default_value") or "").strip(),
                    "description": ""
                }
                if arg["arg_name"] not in ignored_set:
                    args.append(arg) 

            return args
