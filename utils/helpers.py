import json, os, datetime, re
from utils import settings
from rich.console import Console
from rich.traceback import install
install(show_locals=False)

console = Console(stderr=True) # For loging formatted text to the console - with colors

def rich_hr(text, line_style = "dark_green", align="center"):
    '''Print a stylized horizontal ruler (hr) to the console'''
    console.rule(f"[bold green]{text}[/bold green]", style=line_style, align=align)

def rich_print(text, type=None):
    '''Print text to console with formatting and color support

    Color and formatting combo options:
    - red, green, blue, yellow, magenta, cyan, white, black, orange, pink, purple.
      Also supports RGB format: [rgb(255,0,0)]
    - bold, italic, underline, strike

    Usage example: console.print("[bold red]This text will be bold and red[/bold red]")

    REF: https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
    '''

    str = ""
    match type:
        case "warning":
            str = "[bold orange]WARNING:[/bold orange] "
        case "error": 
            str = "[bold red]ERROR:[/bold red] "
        case "note": 
            str = "[bold green]NOTE:[/bold green] "
        case "hint": 
            str = "[bold italic red]HINT:[/bold italic red] "
        case _: # Default case
            if type is not None:
                str = f"[bold]{type}[/bold] " # Custom type...could be anything

    console.print(str + text)

def print_json(json_obj, log=False):
    '''Print json object to screen - expect a valid JSON object as input
    
    log: if True, log json string to file
    '''
    json_str = json.dumps(json_obj, indent=4)
    console.print_json(json_str) # Does not support styling
    if log:
        append_log(json_str)

def print_log(text, type=None):
    '''Print the message to console and append text to log file'''
    rich_print(text, type)
    append_log(text)

def append_log(text):
    '''Append text to log file'''
    write_to_file(settings.PATHS.LOG_FILE.value, f"{get_timestamp()}\n{text}", 'a') # Create file if doesn't exist and append

def open_file(file_name, type="json"):
    '''Open a file, read in all it's content to memory and return the content'''
    try:
        with open(file_name, 'r') as f:
            content = json.load(f) if type == "json" else f.read()
    except FileNotFoundError:
        print("The file was not found: " + file_name)
    except json.JSONDecodeError:
        print("The file is not a valid JSON.")

    return content

def write_to_file(file_name, content, mode='a'):
    '''Write the `content` to the given file path (full path with file name)

    - 'a': append mode (default), will create file if it doesn't exists and append `content` to end of file
    '''
    with open(file_name, mode) as f:
        f.write(content + "\n")

def get_file_name(fpath):
    '''Given a file path, return the file name (e.g.: file.ext)'''
    fname = os.path.basename(fpath)
    return fname

def get_timestamp():
    '''Return a timestamp as of now.'''
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

def ignore_args_check(signature) -> bool:
    '''Check if the signature should be ignored.
    Criteria:
    - Any parameters that contain only or a combo of: "()", "(self)", "(self, *args)", "(self, *args, **kwargs)"
    '''
    
    if re.search(r"\(self(, \*args)?(, \*\*kwargs)?\)|\(\)", signature):
        return True
    
    return False
    