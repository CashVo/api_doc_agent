import ollama

def basic_prompt(user_input: str = ""): 
    response = ollama.generate(
        model = 'llama3.2:latest',
        prompt = user_input,
        #system=system_prompt, # Instructions to the LLM
        options = {
            'temperature': 0,
            "stream": False
        }
    )
    return response['response']
