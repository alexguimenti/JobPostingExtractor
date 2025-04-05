from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os





class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

class ReadReferenceFileTool(BaseTool):
    name: str = Field(default="read_reference_file")
    description: str = Field(default="Read all reference files from the folder and return their contents")


    def _run(self, filename: str) -> str:
        base_path = './reference'
        safe_path = os.path.abspath(os.path.join(base_path, filename))

        # Evita acesso fora da pasta 'reference'
        if not safe_path.startswith(os.path.abspath(base_path)):
            return "Invalid filename. Access is restricted to the 'reference' folder only."

        if not os.path.exists(safe_path):
            return f"File '{filename}' does not exist in the 'reference' folder."

        with open(safe_path, 'r', encoding='utf-8') as f:
            return f.read()
