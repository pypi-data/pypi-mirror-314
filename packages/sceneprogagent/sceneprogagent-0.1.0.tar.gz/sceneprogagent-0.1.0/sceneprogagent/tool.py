from pydantic import BaseModel, Field
from typing import List

class SceneProgTool:
    def __init__(self):
        
        self.name = None
        self.usage = None
        self.io = None
        self.examples = None

    def build_io(self, Inputs, Outputs):
        self.Inputs = Inputs
        self.Outputs = Outputs
        # Generate the text block
        inputs ="\n".join([f"- {name}: {info}" for name, info in dict(Inputs.model_fields.items()).items()])
        outputs = "\n".join([f"- {name}: {info}" for name, info in dict(Outputs.model_fields.items()).items()])
        self.io = f"""
Input:
{inputs}
Output:
{outputs}
"""
    def __str__(self):
        return f"{self.name}: {self.usage}\n{self.io}\n{self.examples}"
    
    def validate_arguments(self, Inputs):
        pass

    def build_response(self, status, message, solution, result):
        class Response:
            def __init__(self, status, message, solution, result):
                self.status = status
                self.message = message
                self.solution = solution
                self.result = result
        return Response(status, message, solution, result)