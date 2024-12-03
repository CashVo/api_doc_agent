import ollama

class LLMManager():
    def __init__(self):
        self.model_info = {
            "llm": "llama3.2", # Default model
            "embed": "",
            "tokenizer": "",
            "system_instructions": '''I am an expert coder and teacher of programming languages. 
            I can provide accurate and helpful information about Python-specific code snippets, explanations, and debugging.
            ''',
            'options': {
                'temperature': 0,
                "stream": False
            }
        }

    def prompt(self, query, model = None, options = None, system_prompt = None):
        '''Prompt the LLM using the provided `query`
        @args
        role: define persona for the LLM (e.g.: Assistant, User, Teacher, Coder, Editor)
        model: name of a model (e.g.: llama3.2, codellama, qwen2.3-coder)
        options: a JSON object (e.g.: {'temperature': 0, 'stream': False})
        '''
                
        response = ollama.generate(
            model = model if model is not None else self.model_info["llm"],
            prompt = query,
            system = system_prompt if system_prompt is not None else self.model_info["system_instructions"],
            options = options if options is not None else self.model_info['options']
        )

        return response