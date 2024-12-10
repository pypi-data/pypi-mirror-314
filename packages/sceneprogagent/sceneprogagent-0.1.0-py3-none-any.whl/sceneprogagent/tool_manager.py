from sceneprogllm import LLM
from .utils import print_colored

class ToolManager:
    def __init__(self, name, silent=False):
        self.name = name
        self.silent = silent
        self.tool_description = ""
        self.tool_registry = {}
        self.tool_identifier = LLM(
            name=f"{self.name}_tool_identifier",
            system_desc="Identify the tool needed to execute the query. Your answer should be a dict like 'tool': 'tool_name'. Note that only a single tool should be identified.",
            response_format="json",
            json_keys=['tool']
        )

        self.tool_argument_extractor = LLM(
            name=f"{self.name}_tool_argument_extractor",
            system_desc="Extract the arguments needed to execute the identified tool. Carefully go through the query and identify the necessary arguments for the tool. ",
            response_format="pydantic",
        )

    def register_tool(self, tool):
        self.tool_registry[tool.name] = tool
        self.tool_description += f"""
Tool: {tool.name}
Usage: {tool.usage}
Input/Output: 
{tool.io}
Example of tool usage: 
{tool.examples}
""" 

    def get_tool_name(self, query):
        tool_name = self.tool_identifier.run(query)
        print_colored(f"Tool identified: {tool_name['tool']}", color="green", silent=self.silent)

        count=0
        while True:
            if tool_name['tool'] == "unknown" or count>3:
                return -1, f"Cannot identify appropriate tool for the query: {query}."
            elif tool_name['tool'] in self.tool_registry:
                return 0, tool_name['tool']
            else:
                prompt = f"""
The tool that you identified: {tool_name['tool']} for the query: {query} cannot be found in the tool registry.
Make sure you are identifying the correct tool with the correct name. If the exact tool is not available, try to identify a similar tool.
If you are unable to identify the tool, please return the tool name as 'unknown'.
"""
                tool_name = self.tool_identifier.run(prompt)
                count+=1
            
    def get_tool_arguments(self, tool, context):
        prompt = f"""
You are required to extract arguments for the tool: {tool.name}
Tool Usage Info: {tool.usage}
Following are the I/O for the tool:
{tool.io}
Use the following context to extract the arguments:
{context}
"""
        arguments = self.tool_argument_extractor.run(prompt, pydantic_object=tool.Inputs)
        count=0
        while True:
            try:
                tool.validate_arguments(arguments)   
                break
            except Exception as e:
                prompt = f"""
Your retrieved arguments: {arguments} for the tool: {tool.name} are incorrect. 
Error: {e}
Please try again.
"""
                print_colored(f"Error: {e} occurred while executing the tool: {tool.name} with arguments: {arguments}.", color="red", silent=self.silent)           
                arguments = self.tool_argument_extractor.run(prompt, pydantic_object=tool.Inputs) 
                count+=1

            if count>3:
                print_colored(f"Tool: {tool.name} failed to execute after 3 attempts. Please think of something else.", color="red", silent=self.silent)
                return -1, f"Tool: {tool.name} failed to execute after 3 attempts. Please think of something else."
            
        print_colored(f"Arguments extracted: {arguments}", color="green", silent=self.silent)
        return 0, arguments
    
    def __call__(self, query, context):
        
        status, tool_name = self.get_tool_name(query)
        if status == -1:
            return -1, tool_name
        
        tool = self.tool_registry[tool_name]
        status, arguments = self.get_tool_arguments(tool, context)
        if status == -1:
            return -1, arguments

        response = tool(arguments)
        if response.status == -1:
            msg = f"""
Tried running the tool: {tool.name} with arguments: {arguments} but it failed to execute.
Error: {response.message}
Potential solution: {response.solution}
"""
            print_colored(msg, color="red", silent=self.silent)
            return -1, msg

        return 0, response.result
