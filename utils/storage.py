import os
from utils import settings, helpers

class Storage():
    '''Handle in-memory state information and storage management (right now, we're using File I/O. In future, we will upgrade to a DB)'''

    def __init__(self):
        # Virtual memory
        self.state = {
            "package_content": {} # Store the latest processed content
        }

        # Persistent memory (e.g.: file or db storage)
        self.storage = {
            # Paths to save content state into. 
            # Each path is a step in the parsing process
            "file_paths": { 
                "class_definitions": "data/processed/class_definitions/",
                "gen_descriptions": "data/processed/gen_descriptions/"
            }
        }
    

    def get_state(self, container):
        '''Return reference to a state container'''
        return self.state[container]
        
    def save_state(self, container, content):
        '''Add or append memory to a given container
        
        @params
        `container`: This is the state's key
        `content`: The content of the container (e.g.: str, dict, list, ref)
        '''
        if self.state[container] is not None:
            self.state[container].update(content)
        else:
            self.state[container] = content

    def save_content_state(self, obj, content):
        '''Append new `obj` content to the `package_content` container'''
        self.state["package_content"][obj] = content

    def get_storage(self, container):
        '''Return a reference to a storage container'''
        return self.storage[container]
    
    def get_storage_path(self, fpath):
        '''Return a file path'''
        return self.storage["file_paths"][fpath]
    
    def persist_data(self, content, fpath, fname, mode="w+"):
        '''Write content out to file'''
        fp = self.storage["file_paths"][fpath] + fname
        helpers.write_to_file(fp, content, mode)

    def content_exists(self, fpath, fname):
        '''Return true if a file exists, otherwise, return false'''
        fp = self.storage["file_paths"][fpath] + fname
        return os.path.exists(fp)
    
    # Helpers
    def load_file_list(self, dev_mode):
        '''For development purposes, we are loading a list of files to parse from
        For production, you could manually curate this entire list or 
        just point to a folder and programmatically build this list'''
        files = helpers.open_file("data/content_files.json")
        return files[dev_mode]

    def load_state_content(self, files, fpath):
        '''Load content into container'''
        for file in files:
            fname = helpers.get_file_name(file)
            content = helpers.open_file(f"data/processed/{fpath}/{fname}")

            helpers.rich_print(f"Content loaded: [bold purple]{fname}[/bold purple]", "note")
            self.save_state("package_content", content)