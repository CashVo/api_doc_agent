# Change Log

## 12/13/24
* Added Grader and Editor agents
* After generating the description, we pass the resulting text to GraderAgent
  * If GraderAgent grade the description other then "[GREAT]" then we pass the suggestions into the EditorAgent to regenerate the description based on the suggestions. Otherwise, we keep the original description.
  * Also, we stored the suggestions with the object.
* Moved the "dev_data" inside our project under "data/raw/dev_data". 
* Added a Planner to the DescriptorAgent
  * Update the `tasks` parameter to target which process you want to run (e.g: "get_desription" or "get_suggestions")
  * `get_suggestions`: A new function is added to start the process by prompting the LLM to "plan" and then sending those "suggestions" to the EditorAgent to generate the description.
* Observations:
  * Majority of the grade came back as "[GREAT]" and only a few "[OK]". Somehow, the LLM has switched to be more negative and have been grading the generated desriptions as "[POOR]". Not sure why.
  * Suggestions:
    * Some great suggestions here but applying them would make the descriptions a lot longer.
* Experiments:
    1) Based on the suggestions, I tried deviating the length limit for the different type. For example: (class limits to 2 paragraphs, function limits to 1 paragraph, and args limits to 2 sentences).
    2) Rather then generating the description first, I modified the DescriptorAgent to generate instructions for how to best describe the code. Then, ask the EditorAgent to generate the description. Followed by the grader and invoke the EditorAgent if the grade is not GREAT.
    3) Example: I tried adding an example block and LLM kep regergitating the example text. Not sure why it is treating example text in that way. It was supposed to use it as a guide only. But it is using it as the actual response. [FIXED]

* Commit status:
```
  modified:   README.md
  modified:   agents/base_agent.py
  modified:   agents/descriptor_agent.py
  new file:   agents/editor_agent.py
  new file:   agents/grader_agent.py
  modified:   change_logs.md
  modified:   data/content_files.json
  modified:   data/log.txt
  modified:   data/processed/class_definitions/dev_data/collectors/collectors.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/collectors-descriptor.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/collectors-planner.py   
  deleted:    data/processed/gen_descriptions/dev_data/collectors/collectors.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/collectors1.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/collectors2.py
  modified:   data/processed/gen_descriptions/dev_data/collectors/distributed/utils.py    
  modified:   data/processed/gen_descriptions/dev_data/collectors/utils.py
  new file:   data/raw/dev_data/collectors/__init__.py
  new file:   data/raw/dev_data/collectors/collectors.py
  new file:   data/raw/dev_data/collectors/distributed/__init__.py
  new file:   data/raw/dev_data/collectors/distributed/default_configs.py
  new file:   data/raw/dev_data/collectors/distributed/generic.py        
  new file:   data/raw/dev_data/collectors/distributed/ray.py
  new file:   data/raw/dev_data/collectors/distributed/rpc.py
  new file:   data/raw/dev_data/collectors/distributed/sync.py
  new file:   data/raw/dev_data/collectors/distributed/utils.py
  new file:   data/raw/dev_data/collectors/utils.py
  modified:   utils/helpers.py
  modified:   utils/prompt_helper.py
  modified:   utils/storage.py
```

## 12/11/24
Mainly code restructuring to help streamline work in later steps
* Parser Phase Flow: sequential => user defined
  * Updated this workflow to enable user defined steps. Rather then starting at step 1 each time, the user gets to define where to start. 
  * Mainly to help us move faster during the development phase. Since we write the results to file at each step, there is no need to start from the beginning every time.
* Memory Management: Added structure to help manage state and storage memory
  * Added a `Storage` class to help us manage memory
    * `state`: in-memory storage
    * `storage`: persistent storage (e.g.: file or db)
* Parsing and storage: Instead of writing everything out to one file, which can be gigantic for an entire API, we will now store each processed packge in its own file. However, we will still maintain the entire API content in one JSON object in our `package_content` obj for downstream processing.
  * For testing purposes and to help iterate faster (as well as focused debugging), I added a `dev_mode` flag that points to a different set of files to process.
  * archived folder: I have moved old parsed files into an `archived` folder. 
* Include docstring: Will now parse for any docstring and store it with the object.
* Commit status:
```
  modified:   README.md
  modified:   agents/descriptor_agent.py
  modified:   change_logs.md
  modified:   content_curration_workflow.py
  modified:   data/content_files.json
  modified:   data/log.txt
  renamed:    data/processed/ast_out.json -> data/processed/archive/ast_out.json
  renamed:    data/processed/class_definitions-1.json -> data/processed/archive/class_definitions-1.json
  renamed:    data/processed/class_definitions-2.json -> data/processed/archive/class_definitions-2.json
  renamed:    data/processed/class_definitions-3.json -> data/processed/archive/class_definitions-3.json
  new file:   data/processed/archive/class_definitions.json
  renamed:    data/processed/gen_desriptions-1.json -> data/processed/archive/gen_desriptions-1.json
  renamed:    data/processed/gen_desriptions-2-args.json -> data/processed/archive/gen_desriptions-2.json
  renamed:    data/processed/gen_desriptions-3-arg.json -> data/processed/archive/gen_desriptions-3-arg.json
  renamed:    data/processed/gen_desriptions.json -> data/processed/archive/gen_desriptions.json
  renamed:    data/processed/class_definitions.json -> data/processed/archive/gen_desriptions4.json
  new file:   data/processed/class_definitions/dev_data/collectors/collectors.py
  new file:   data/processed/class_definitions/dev_data/collectors/distributed/utils.py
  new file:   data/processed/class_definitions/dev_data/collectors/utils.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/collectors.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/distributed/utils.py
  new file:   data/processed/gen_descriptions/dev_data/collectors/utils.py
  modified:   flask_app.py
  modified:   utils/ast_parser.py
  modified:   utils/helpers.py
  modified:   utils/settings.py
  new file:   utils/storage.py
```

## 12/4/24
* Prompt templates: free-form => XML
  * Converting the template from free-form text format to a structured XML format
  * Had an issue LLM treating `<examples>` too literally where it often times uses the example description exactly for a thing that doesn't even relate
  * I removed the `<examples>` block and now the descriptions for each item are now much better.
* Args processing: all at once => one at a time
  * I parsed the func signature to get each arguments into its own JSON object and prompted the LLM to provide desription to each - one at a time.
    * Description seems to be much higher quality and more accurate
    * Steps goes from 91 to 120....but total elapsed time to prompt LLM in both cases comes out to be the same: 62mins ... fastest run finished at 45mins
  * Got this to work by using just 1 prompt template for all 3 cases (class, function, and parameter) - since the end goal is to ask LLM to generate a description, there is no need to treat that task special
    * Args are each captured more accurately during the parse phase and we can use all the info from there to help form the final description structure at the end.
    * here's an example:
    ```
    {
      "function_name": "set_seed",
      "args": [
          {
              "arg_name": "seed",
              "return_type": "int",
              "default_value": "",
              "description": "This parameter is used to initialize the random number generator, allowing for reproducibility of results and enabling users to set a specific starting point for their random number generation."
          },
          {
              "arg_name": "static_seed",
              "return_type": "bool",
              "default_value": "False",
              "description": "This parameter is used to enable or disable the use of a static seed for random number generation, allowing for reproducibility and deterministic behavior in simulations."
          }
      ],
      "signature": "set_seed(self, seed: int, static_seed: bool=False) -> int",
      "function_code": "def set_seed(self, seed: int, static_seed: bool=False) -> int:\n    return super().set_seed(seed, static_seed)",
      "description": "This function is used to initialize a random number generator with a specified seed value, allowing for reproducibility and control over the sequence of random numbers generated. The function takes an optional parameter 'static_seed' which defaults to False, indicating whether the seed should be set as static or not."
    }
    ```
* Commit status:
  ```
  modified:   agents/descriptor_agent.py
  modified:   data/log.txt
  new file:   data/processed/class_definitions-1.json
  new file:   data/processed/class_definitions-2.json
  new file:   data/processed/class_definitions-3.json
  modified:   data/processed/class_definitions.json
  new file:   data/processed/gen_desriptions-2-args.json
  modified:   data/processed/gen_desriptions.json
  modified:   utils/ast_parser.py
  modified:   utils/prompt_helper.py
  modified:   change_logs.md
  ```

## 12/2/24
* Workflow: Clarify what a step is and added function calling. Do away with `workflow_manager` because it does not make sense in the current implementation. Might add it back in later.
* Settings and helpers: started to use these more in this check in. Plans to continue adding to these spaces as needed (e.g.: Might add a "storage" space to the settings to manage in-memory storage)
* Rich and TQDM: Added these two libraries to help make reading console more pleasent...also, status bars help to see progress as prompting LLM can take a long time
* log.txt: started to add messages to log file. I'll try to clean this up regularly so it doesn't get too large in size.
* Commit status:
```
    new file:   agents/base_agent.py
    new file:   agents/descriptor_agent.py
    modified:   agents/doc_parser_agent.py
    modified:   agents/llm_manager.py
    new file:   content_curration_workflow.py
    modified:   data/content_files.json
    new file:   data/log.txt
    renamed:    data/processed/ast_output.json -> data/processed/ast_out.json
    new file:   data/processed/class_definitions.json
    new file:   data/processed/gen_desriptions-1.json
    new file:   data/processed/gen_desriptions.json
    modified:   flask_app.py
    modified:   requirements.txt
    modified:   utils/ast_parser.py
    modified:   utils/helpers.py
    modified:   utils/settings.py
    new file:   utils/workflow.py
    new file:   utils/workflow_manager.py
    deleted:    workflow_manager.py
```

## 11/21/24: Code Refactoring - focused on workflow setup
* Refactor how `workflow_manager` work. Moved `workflow_agent` into this class an removed the `workflow_agent` file
  * For phase 1, not much user interaction and the WorkflowManager just builds a set of steps and execute one in order
  * As we go through the steps, we will need to figure out how to pause the step and take user input and then continue with that step...hopefully this will become more clear as we build out the work for subsequent steps.
* Break the change log out into it's own file (this one) so we don't over crowd README
* Add a workflow diagram for phase 1 in the README

## 11/20/24: Added Workflow and Parsing agents
* Workflow Agent: Got a basic workflow manager setup to handle the content parsing step
* Parsing Agent:  
  * I got two parsing functions defined. One using AST and the other using LLM.
  * At first, I thought I could pass in the entire code file along with prompt template to get the LLM to do all the parsing and writing in one go. But, it's taking way too long to response. Longest wait time was about 3hrs and not even returning with a response. So, I am not sure what it was able to generate in that run. It would save us a lot of coding if I have more powerful hardware to let the LLM do most of the work.
  * So, the fallback plan is manually parse the code file for class and function signatures. Then, iteratively prompt the LLM to provide the descriptions
