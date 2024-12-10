'''
Features of the simple agent
1. Tool usage (done)
2. Handle tool failure (done)
3. code execution
4. Should be able to plan (done)
5. Ability to refine response
6. able to collaborate with other agents
7. Implements RAG
8. 
'''
from sceneprogllm import LLM
from .planner import Planner
from .tool_manager import ToolManager
from .utils import print_colored

class SceneProgAgent:
    def __init__(self, name, role, description, planning_examples=None, silent=False):
        self.name = name
        self.role = role
        self.description = description
        self.silent = silent
        self.planning_examples = planning_examples
        self.tool_manager = ToolManager(name=self.name)

        description = f"""
Your name: {name}
Your Role: {role}
Task Description: {description}
"""
        self.llm = LLM(
            name=name,
            system_desc=description,
            response_format="text",
        )

        self.clear_memory()

    def clear_memory(self):
        self.memory = ""

    def clear_scratchpad(self):
        self.scratchpad = ""

    def register_tool(self, tool):
        self.tool_manager.register_tool(tool)

    def add_to_memory(self, speaker, message):
        self.memory += f"{speaker}: {message}\n"
    
    def add_to_scratchpad(self, speaker, message):
        self.scratchpad += f"{speaker}: {message}\n"

    def try_executing_plan_step(self, plan, plan_idx, query):
        step = plan[plan_idx-1]
        self.add_to_scratchpad("You", "Executing step: "+step)
        prompt = f"""
The activity has been so far:
{self.scratchpad}
You are required to generate a brief reponse which contains sufficient information to execute the following step:
{step}
"""
        context = self.llm.run(prompt)
        status, result = self.tool_manager(step, context)
        if status == -1:
            self.add_to_scratchpad("You", "Error found: "+result)
            return -1, result
        self.add_to_scratchpad("You", "Step executed successfully.")
        self.add_to_scratchpad("You", "Result: "+str(result))
        print_colored(f"Result: {result}", color="magenta", silent=self.silent)
        return status, result
        
    def init_planner(self):
        self.planner = Planner(name=f"{self.name}_planner", planning_examples=self.planning_examples, tool_description=self.tool_manager.tool_description)

    def __call__(self, query):
        print_colored(f"Query: {query}", color="blue", silent=self.silent)
        self.clear_scratchpad()

        self.add_to_memory("User", query)
        self.add_to_scratchpad("User", query)

        plan, plan_idx = self.planner(query)
        print_colored(f"Plan: {plan}, Plan Index: {plan_idx}", color="green", silent=self.silent)
        if plan == ["CANNOT PLAN"]:
            msg = "I'm sorry, I don't have sufficient information or tools to answer this query."
            self.add_to_memory("You", msg)
            return -1, msg
        
        self.add_to_scratchpad("Planner", "Following is the plan to achieve the task:"+"\n".join(plan))
        
        while True:
            status, result = self.try_executing_plan_step(plan, plan_idx, query)
            if status == -1:
                plan, plan_idx = self.planner.refine_plan(query, plan, plan_idx, result)
                print_colored(f"Refined Plan: {plan}, Plan Index: {plan_idx}", color="green", silent=self.silent)
                if plan == ["CANNOT PLAN"]:
                    msg = "I'm sorry, I don't have sufficient information or tools to answer this query."
                    self.add_to_memory("You", msg)
                    return -1, msg
                
                self.add_to_scratchpad("Planner", "Following is the refined plan to achieve the task:"+"\n".join(plan))
            else:
                plan_idx += 1
            
            if plan_idx > len(plan):
                break

        self.add_to_memory("You", "Task completed successfully.")
        return result