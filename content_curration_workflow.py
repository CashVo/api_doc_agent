from utils import workflow, helpers, settings
import os, json

workflow = workflow.Workflow()

def start_curration_workflow(agents):
    '''Build a default set of steps and start the initial workflow''' 
    
    # PASE 1: Steps in the content curration phase
    # Parsed content as JSON string

    # NOTE: About the code structure
    # packages: contains a list of classes inside a .py file (use file name as key)
    # classes: contains a list of functions
    # functions: contains a list of arguments related to the function
    # Example JSON structure:
    # {
    #      "package_name": [
    #             {
    #                "classes": [
    #                     {
    #                         "class_name": "name of class"
    #                         "functions": [
    #                              {
    #                                 "function_name": ""
    #                                 "args": [],
    #                                 "signature": "",
    #                                 ...
    #                              }                                
    #                         ]                     
    #                     }
    #                 ]
    #             },
    #             {
    #                 "function_name": "",
    #                 "args": [],
    #                 "signature": ""
    #             }
    #      ]
    # }

    # STEP 1) Parse code signatures and output results as JSON file
    helpers.rich_hr('Step 1 - CURATION PHASE')
    package_content = { } 

    if os.path.exists(settings.PATHS.PARSED_FILE.value): # skip parsing if content already parsed
            helpers.rich_print(f"* Parsed file already exists: [italic magenta]{settings.PATHS.PARSED_FILE.value}[/italic magenta]. [red]Delete[/red] this file to reparse code.", "note")   
            helpers.rich_print("Load content into memory", 'note')
            package_content = helpers.open_file(settings.PATHS.PARSED_FILE.value, 'json') # Load content to memory
    else: # Parse        
        files = helpers.open_file(settings.PATHS.CONTENT_FILE.value) # Get a list of file paths to parse
        for file in files['files']: # Go through each file
            helpers.rich_print(f'Parsing file [magenta]{file}[/magenta]', 'CURRATION:')
            fname = helpers.get_file_name(file)
            raw_content = helpers.open_file(file, 'py') # Load all raw content to memory    
            results = agents['parserAgent'].parse(raw_content)
            package_content[fname] = results # save results to memory
            
            # Logging: Save results to log file - append mode
            results_as_str = json.dumps(results, indent=4)
            helpers.append_log(fname + ": " + results_as_str) # write to log file
        # Write parsed content to file
        helpers.write_to_file(settings.PATHS.PARSED_FILE.value, json.dumps(package_content, indent=4), 'w+') # Over-write existing content, if any
        helpers.rich_print(f'Results writen to file - [magenta]{settings.PATHS.PARSED_FILE.value}[/magenta]', 'note')
    helpers.rich_print('Step 1 - done', 'CURATION PHASE')

    # 2) Add description for each class and method (update JSON file)
    helpers.rich_hr('Step 2 - CURATION PHASE')
    agents['descriptorAgent'].generate_descriptions(package_content)
    helpers.write_to_file(settings.PATHS.GEN_DESCRIPTIONS.value, json.dumps(package_content, indent=4), 'w+') # Over-write existing content, if any

    helpers.rich_print('Step 2 - done', 'CURATION PHASE')
    
    # 3) Generate class overview and introductory information (Update JSON file)
    helpers.rich_hr('Step 3 - CURATION PHASE')

    helpers.rich_print('Step 3 - done', 'CURATION PHASE')

    # 4) Generate code samples for each class and method (Update JSON file)
    # 5) Generate educational content such as "how to" topics and output as JSON file
    # 6) Publish API content in various formats

    # Defile the steps in terms of sequential tasks to accomplish
    # This is phase 1
    # steps = [
    #     workflow.create_step("PARSE", step1, agents['parserAgent']),
    #     workflow.create_step("DESCRIBE", agents['descriptorAgent'].generate_descriptions),
    #     # self.workflow.define_step(ACTIONS.OVERVIEW, ),
    #     # self.workflow.define_step(ACTIONS.CODE, ),
    #     # self.workflow.define_step(ACTIONS.EDU, ),
    #     # self.workflow.define_step(ACTIONS.API, ),
    # ]
    # workflow.add_steps(steps)
    
    # Start the workflow
    # while step := workflow.get_next_step():
    #     if step is not None:
    #         step['call_function']() # Execute the func in the step
    #     else:
    #         break
    
    