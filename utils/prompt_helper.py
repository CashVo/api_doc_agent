
class PROMPT_TEMPLATES:

    def get_template(self, template_name, **kwargs):
        '''Return the template string and apply their keyword arguments to placeholders'''

        if template_name == "GENERATE_DESCRIPTION":
            return self.GENERATE_DESCRIPTION.format(**kwargs)
        elif template_name == "GENERATE_ARGS_DESCRIPTION":
            return self.GENERATE_ARGS_DESCRIPTION.format(**kwargs)
        elif template_name == "GRADER":
            return self.GRADER.format(**kwargs)
        elif template_name == "EDITOR":
            return self.EDITOR.format(**kwargs)
        elif template_name == "PLANNER":
            return self.PLANNER.format(**kwargs)
        else:
            return "ERROR: Unknown template name - " + template_name


    # Instructions for generating descriptions
    GENERATE_DESCRIPTION = '''
<purpose>
You are an API Documenation Writer. Generate a description for this {objtype}: "{objname}". 
Use the provided <instructions> and <context> content to guide you in your work.
</purpose>
<instructions>
    <instruction>Describe the purpose and functionality of the {objtype}: "{objname}"</instruction>
    <instruction>Start the description with: "This {objtype} "</instruction>
    <instruction>Return your generated description only. Do not wrap any tags around your response text.</instruction>
    <instruction>Limit response to {limit} or less</instruction>
</instructions>

<context>
{context}
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
You are an API Documenation Writer. Generate a description for this {objtype}: "{objname}".
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
{context}
</contex>
'''


    # Instructions for grader agent
    GRADER = '''
<purpose>
You are a content reviewer. As a results, you provide a grade and suggestion for improvements. 
Given the generated <content> for a {context}, assess how accurate the content is against the <code> it is describing.
Use the provided <instructions>, <content>, and <code> sections to guide you in your work.
</purpose>
<instructions>
    <instruction>Give this <content> a grade and your reason for the grade given. 
    Use these terms for your grade: [POOR | OK | GREAT]
    * "POOR" means the description does not match the code
    * "OK" means the description matched the code about 50%
    * "GREAT" means the description match the code perfectly
    </instruction>
    <instruction>Provide suggestions for improvements (no more then 3 suggestions)</instruction>
    <instruction>Provide your response in this format. It's IMPORTANT that grade is given inside square brackets: 
    [GRADE] - <Reason_for_grade>
    Improvement Suggestions:
    1) Suggestion text
    2) Suggestion text
    3) Suggestion text
    </instruction>
</instructions>
<content>
{content}
</content>
<code>
{code}
</code>
'''
    # Instructions for editor agent
    EDITOR = '''
<purpose>
You are a content editor. Given the generated <content> and a list of suggestions, generate a description based on these suggestions.
Use the provided <instructions>, <content>, <code>, and <suggestions> sections to guide you in your work.
</purpose>
<instructions>
    <instruction>Return your generated description only. Do not wrap any tags around your response text.</instruction>
    <instruction>Limit response to {limit} or less</instruction>
</instructions>
<content>
{content}
</content>
<code>
{code}
</code>
<suggestions>
{suggestions}
</suggestions>
'''

    # Instructions for editor agent
    PLANNER = '''
<purpose>
You are a content planner for an API documentation set. 
Use the <code> block as context, provide a list of suggestions for what to include in the description of the `{objtype} {objname}`.
Use the provided <instructions>, and <code> sections to guide you in your work.
</purpose>
<instructions>
    <instruction>Return your generated description only. Do not wrap any tags around your response text.</instruction>
    <instruction>Limit your suggestions to 3 or less</instruction>
</instructions>
<code>
{context}
</code>
'''