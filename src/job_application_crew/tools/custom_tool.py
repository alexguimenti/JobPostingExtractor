from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import shutil
from datetime import datetime
import re





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


class BackupMarkdownFilesTool(BaseTool):
    name: str = "backup_markdown_files"
    description: str = "Backup markdown files to a specified destination and clean up source files"
    
    def _run(self, source: str = None, destination_base: str = None, job_research_filename: str = "job_research.md") -> str:
        # Use default values if not provided
        if source is None:
            # Usando caminho absoluto conforme especificado
            source = "C:\\Users\\alexg\\Documents\\crewai\\job_application_crew"
        if destination_base is None:
            # Destino atualizado conforme solicitado
            destination_base = "D:\\Documents\\Jobs Application"
        
        print(f"Source directory: {source}")
        print(f"Destination base: {destination_base}")
        
        # Full path to the job_research.md file
        job_research_path = os.path.join(source, job_research_filename)
        print(f"Looking for job research file at: {job_research_path}")

        # Helper function to extract company name from job_research.md
        def extract_company_name(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        # Match Markdown and plain text formats
                        match = re.search(r"\*\*?Company Name\*\*?:\s*(.*)", line, re.IGNORECASE)
                        if not match:
                            match = re.search(r"Company Name:\s*(.*)", line, re.IGNORECASE)
                        if match:
                            name = match.group(1).strip()
                            name = re.sub(r"\s+", "_", name)  # Replace spaces with underscores
                            name = re.sub(r"[^\w_]", "", name)  # Remove special characters
                            name = name.lstrip("_")  # Remove underscores from the beginning
                            return name
            except FileNotFoundError:
                print(f"File not found: {filepath}")
            return None

        # Determine folder name based on company name or timestamp
        company_name = extract_company_name(job_research_path)
        if not company_name:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            folder_name = f"backup_{timestamp}"
        else:
            folder_name = company_name

        # Create the destination directory
        destination = os.path.join(destination_base, folder_name)
        os.makedirs(destination, exist_ok=True)
        print(f"Created destination directory: {destination}")

        # Check if source directory exists
        if not os.path.exists(source):
            print(f"Source directory does not exist: {source}")
            return f"Error: Source directory does not exist: {source}"

        # Copy all .md files from source to destination
        copied_files = []
        for file in os.listdir(source):
            if file.endswith(".md"):
                source_path = os.path.join(source, file)
                destination_path = os.path.join(destination, file)
                shutil.copy2(source_path, destination_path)
                copied_files.append(file)
                print(f"Copied: {file}")

        result_message = f"All .md files have been successfully copied to '{destination}'."

        # Files to delete after successful copy
        files_to_delete = ["resume.md", "cover_letter.md", "job_research.md", "profile.md", "salary.md"]

        for file_to_delete in files_to_delete:
            if file_to_delete in copied_files:
                try:
                    os.remove(os.path.join(source, file_to_delete))
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Failed to delete {file_to_delete}: {e}")

        return result_message