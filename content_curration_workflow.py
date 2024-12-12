from utils import workflow, helpers, settings
import os, json, time

workflow = workflow.Workflow()

def start_curration_workflow(agents, memory):
    '''Build a default set of steps and start the initial workflow''' 
    

    # "files" = prod mode 
    # "dev_files" = dev mode
    # In dev mode, we truncated the code file for brievity and to help us target on very specific code for test and debugging
    dev_mode = "dev_files"
    files = memory.load_file_list(dev_mode) # Get a list of file paths to parse
    fname = helpers.get_file_name(files[0])

    steps = ["", "class_definitions", "gen_descriptions"]
    exit = False

    # PASE 1: Steps in the content curration phase
    # Parsed content as JSON string
    while not exit:
        helpers.rich_hr('[bold  green on white]=== CURATION PHASE ===[/bold green on white]')
        action = helpers.ask_user("What step would you like to start with: ")
        match action:
            case "exit":
                exit = True
                break
            case "step1":
                # STEP 1) Parse code signatures and output results as JSON file
                helpers.rich_hr('Step 1 - CURATION PHASE')
                if memory.content_exists(steps[1], fname): # skip parsing if content already parsed
                        helpers.rich_print(f"* Parsed file already exists in [italic magenta]class_definitions[/italic magenta] folder. [red]Delete[/red] this [red]{fname}[/red] to reparse code.", "note")   
                        helpers.rich_print("Loading content into memory", 'note')
                        memory.load_state_content(files, steps[1])
                else: # Parse
                    for file in files: # Go through each file
                        fname = helpers.get_file_name(file)
                        helpers.rich_print(f'Parsing file [magenta]{file}[/magenta]', 'CURRATION:')
                        raw_content = helpers.open_file(file, 'py') # Load raw code to memory    
                        results = agents['parserAgent'].parse(raw_content) # Parse the file
                        memory.save_content_state(fname, results) # Save to state
                        
                        # Logging: Save results to log file - append mode
                        results_as_str = json.dumps({fname : results}, indent=4)
                        helpers.append_log(fname + ": " + results_as_str) # write to log file
                        memory.persist_data(results_as_str, steps[1], fname) # Write to storage
                        helpers.rich_print(f'Results stored at [magenta]{fname}[/magenta]', 'note')
                helpers.rich_print('Step 1 - done', 'CURATION PHASE')
            case "step2":
                # 2) Add description for each class and method (update JSON file)
                tStart = time.time()
                helpers.rich_hr('Step 2 - CURATION PHASE')
                if memory.content_exists(steps[2], fname):
                    helpers.rich_print(f"* Description file already exists: [italic magenta]gen_definitions[/italic magenta]. [red]Delete[/red] this [red]{fname}[/red] to reparse code.", "note")   
                    helpers.rich_print("Load content into memory", 'note')
                    memory.load_state_content(files, steps[2])
                else:
                    for file in files: # Go through each file
                        fname = helpers.get_file_name(file)
                        helpers.rich_print(f'Generating descriptions for [magenta]{file}[/magenta]', 'CURRATION:')
                        agents['descriptorAgent'].generate_descriptions(memory.get_state("package_content")[fname])
                        results = memory.get_state("package_content")[fname]
                        results_as_str =  json.dumps({fname : results}, indent=4)
                        helpers.append_log(fname + ": " + results_as_str) # write to log file
                        memory.persist_data(results_as_str, steps[2], fname) # Write to storage
                        helpers.rich_print(f'Results stored at [magenta]{fname}[/magenta]', 'note')

                elapsed_time = (time.time() - tStart) / 60 # Convert to minutes
                helpers.print_log(f"Total elapsed time (GenDescription Workflow): {elapsed_time} min")
                helpers.rich_print('Step 2 - done', 'CURATION PHASE')
            case "step3":
                # 3) Generate class overview and introductory information (Update JSON file)
                helpers.rich_hr('Step 3 - CURATION PHASE')

                helpers.rich_print('Step 3 - done', 'CURATION PHASE')
            case _:
                helpers.rich_print(f"Unknown action '{action}'. Try 'step1'", "error")

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
    
    