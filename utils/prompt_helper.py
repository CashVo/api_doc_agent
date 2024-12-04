
class PROMPT_TEMPLATES:

    def get_template(self, template_name, **kwargs):
        '''Return the template string and apply their keyword arguments to placeholders'''

        if template_name == "GENERATE_DESCRIPTION":
            return self.GENERATE_DESCRIPTION.format(**kwargs)
        elif template_name == "GENERATE_ARGS_DESCRIPTION":
            return self.GENERATE_ARGS_DESCRIPTION.format(**kwargs)
        else:
            return "ERROR: Unknown template name - " + template_name


    # Instructions for generating class and function descriptions
    GENERATE_DESCRIPTION = '''
<purpose>
Generate a description for this {objtype}: "{objname}". 
Use the provided instructions and contextual content to guide you in your work.
</purpose>
<instructions>
    <instruction>Describe the purpose and functionality of the {objtype}: "{objname}"</instruction>
    <instruction>Start the description with: "This {objtype} is "</instruction>
    <instruction>Return your generated description only. Do not wrap any tags around your response text.</instruction>
</instructions>

<context>
{content}
</context>
'''
# <examples>
#     <example>This class is a data collector for multi-agent environments, designed to collect and store experiences from multiple agents in parallel, allowing for efficient training of multi-agent reinforcement learning models.</example>
#     <example>This function is used to clean up resources and finalize the shutdown of a PyTorch model or module instance before calling its parent class's `shutdown` method.</example>
#     <example>Whether the static seed is used.</example>
#     <example>If provided, indicates the total number of frames returned by the collector during its lifespan.</example>
# </examples>


    # Instruction for generating argument descriptions
    GENERATE_ARGS_DESCRIPTION = '''
<purpose>
Generate a description for this {objtype}: "{objname}".
Use the provided instructions, example output, and contextual content to guide you in your work.
</purpose>
<instructions>
    <instruction>Describe the purpose and functionality of the {objtype}: "{objname}"</instruction>
    <instruction>Return the description in this format: (<return_type>) - <description - indicate 'optional' if it is explicitly provided> (<default: if any>)</instruction>
    <instruction>Return your generated description only. Do not wrap any tags around your response text.</instruction>
</instructions>
<examples>
    <example>(bool) - Whether the static seed is used. (default: False)</example>
    <example>(Optional[int]) - If provided, indicates the total number of frames returned by the collector during its lifespan. (default: -1 (never ending collector))</example>
</examples>
<context>
{content}
</contex>
'''