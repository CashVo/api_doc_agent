
class WorkflowAgent:
    def __init__(self):
        self.steps = []
        self.current = -1 # starts at 0


    def define_step (action = "none"):
        '''Define a custom step or use defaults'''
        step = {
            "action": action
        }
        return step 
    
    def add_step(self, step):
        '''Add a new step to the end of the list'''
        self.steps.append(step)

    def get_next_step(self):
        '''Return the next step and advance the `current` position forward by 1'''
        if (self.current + 1) < len(self.steps):
            self.current += 1
            return self.steps[self.current]
        else:
            return self.define_step()

