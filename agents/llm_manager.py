import ollama

class LLMManager():
    def __init__(self):
        self.model_info = {
            "llm": "llama3.2",
            "embed": "",
            "tokenizer": "",
            "system_instructions": '''I am an expert coder and teacher of programming languages. 
            I can provide accurate and helpful information about Python-specific code snippets, explanations, and debugging.
            '''
        }

    def prompt(self, query, system_prompt = None):
        if(system_prompt is None):
            system_prompt = self.model_info["system_instructions"]
        
        response = ollama.generate(
            model = self.model_info["llm"],
            prompt = query,
            system=system_prompt, # Instructions to the LLM
            options = {
                'temperature': 0,
                "stream": False
            }
        )

        return response