

class Workflow:
    def __init__(self):
        self.clear_steps() # Clears and initialize vars


    def create_step(self, name, function, choices = None, *args, **kwargs):
        '''Create and return a new step'''
        step = {
            "name": name, # Name of the step
            "call_function": function, # A function to execute
            "args": list(args),
            "kwargs": kwargs,
            "choices": choices, # Decide which action to take from a list of choices
        }
        return step 
    
    def add_step(self, step):
        '''Add a new step to the end of the list'''
        self.steps.append(step)

    def add_steps(self, steps):
        '''Start a new workflow with the given list of steps'''
        self.steps = steps
        self.current = -1 # Reset to new workflow state

        # NOTE: May need to save the old steps in case we need to continue

    def clear_steps(self):
        '''Clear the queue'''
        self.steps = []
        self.current = -1 # starts at 0

    def get_next_step(self):
        '''Return the next step and advance the `current` position forward by 1'''
        if (self.current + 1) < len(self.steps):
            self.current += 1
            return self.steps[self.current]
        else:
            return None

    def get_step(self, name):
        '''Return the step with the associated `name`. Otherwise, return `None`'''
        for i, s in self.steps:            
            if name == s['name']:
                return s
            else:
                return None
        
    def update_step(self, name, step):
        '''Update an existing step'''
        updated = False
        for i, s in self.steps:            
            if name == s['name']:
                s = step
                updated = True
                break
        
        return updated
