import os
import re
import shutil
from datetime import datetime
from typing import Type

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# Load environment variables from .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
load_dotenv(dotenv_path=dotenv_path)

openai_key = os.getenv("OPENAI_API_KEY")


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
    """Tool to read files from the reference folder only."""
    name: str = "read_reference_file"
    description: str = "Read all reference files from the folder and return their contents"

    def _run(self, filename: str) -> str:
        base_path = './reference'
        safe_path = os.path.abspath(os.path.join(base_path, filename))

        # Prevent access outside the 'reference' folder
        if not safe_path.startswith(os.path.abspath(base_path)):
            return "Invalid filename. Access is restricted to the 'reference' folder only."

        if not os.path.exists(safe_path):
            return f"File '{filename}' does not exist in the 'reference' folder."

        with open(safe_path, 'r', encoding='utf-8') as f:
            return f.read()

class ConvertMarkdownToHTMLTool(BaseTool):
    name: str = "convert_markdown_to_html"
    description: str = "Converts a resume written in Markdown to a modern, single-page A4 HTML format using a predefined template."
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _load_html_template(self) -> str:
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "templates",
            "resume_template.html"
        )
        template_path = os.path.abspath(template_path)

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def read_markdown_file(self, file_path: str) -> str:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading file '{file_path}': {e}")
                return ""
        else:
            print(f"Warning: The file '{file_path}' was not found.")
            return ""

    def save_html_file(self, html_content: str, output_path: str) -> None:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"Error writing HTML file '{output_path}': {e}")

    def convert_and_save(self, markdown_path: str, html_output_path: str) -> None:
        markdown_content = self.read_markdown_file(markdown_path)

        if markdown_content:
            html_result = self._run(markdown_content)
            self.save_html_file(html_result, html_output_path)
            print(f"HTML successfully saved to '{html_output_path}'")
        else:
            print(f"Skipping conversion. Markdown file '{markdown_path}' not found or empty.")

    def _run(self, argument: str) -> str:
        client = OpenAI(api_key=openai_key)

        html_template = self._load_html_template()

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You will receive a resume in Markdown. Convert it into a single-page A4 HTML using the following template:\n\n{html_template}\n\nInstructions: Do not alter the resume text content. Optimize layout and fit in one page."
                },
                {
                    "role": "user",
                    "content": argument
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()



class BackupMarkdownFilesTool(BaseTool):
    """Tool to backup Markdown and YAML config files to a specified destination."""
    name: str = "backup_markdown_files"
    description: str = "Backup markdown and config files to a specified destination and clean up markdown source files"

    def _run(self, source: str = None, destination_base: str = None, job_research_filename: str = "job_research.md") -> str:
        source = r"C:\Users\alexg\Documents\Projects\job_application_crew"
        destination_base = r"C:\Users\alexg\OneDrive\Pessoal\Jobs Application"


        print(f"Source directory: {source}")
        print(f"Destination base: {destination_base}")

        job_research_path = os.path.join(source, job_research_filename)
        print(f"Looking for job research file at: {job_research_path}")

        company_name = self._extract_company_name(job_research_path)
        folder_name = company_name or f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        destination = os.path.join(destination_base, folder_name)
        os.makedirs(destination, exist_ok=True)
        print(f"Created destination directory: {destination}")

        if not os.path.exists(source):
            return f"Error: Source directory does not exist: {source}"

        # Copy markdown files
        copied_md_files = self._copy_files_by_extension(source, destination, ".md")

        # Copy YAML files from config folder only
        config_folder = os.path.join(source, "src", "job_application_crew", "config")
        self._copy_yaml_files(config_folder, destination)

        # Delete only the copied markdown files
        self._delete_source_files(source, copied_md_files)

        return f"All .md and config .yaml files have been successfully copied to '{destination}'."

    def _extract_company_name(self, filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.search(r"\*\*?Company Name\*\*?:\s*(.*)", line, re.IGNORECASE) or \
                            re.search(r"Company Name:\s*(.*)", line, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        name = re.sub(r"\s+", "_", name)
                        name = re.sub(r"[^\w_]", "", name)
                        return name.lstrip("_")
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        return None

    def _copy_files_by_extension(self, source: str, destination: str, extension: str) -> list:
        copied_files = []
        for file in os.listdir(source):
            if file.endswith(extension):
                src_file = os.path.join(source, file)
                dest_file = os.path.join(destination, file)
                shutil.copy2(src_file, dest_file)
                copied_files.append(file)
                print(f"Copied: {file}")
        return copied_files

    def _copy_yaml_files(self, config_folder: str, destination: str) -> None:
        """Copy only agents.yaml and tasks.yaml from the config folder to destination."""
        yaml_files_to_copy = ["agents.yaml", "tasks.yaml"]

        if not os.path.exists(config_folder):
            print(f"Config folder not found: {config_folder}")
            return

        for file in os.listdir(config_folder):
            if file in yaml_files_to_copy:
                src_file = os.path.join(config_folder, file)
                dest_file = os.path.join(destination, file)
                shutil.copy2(src_file, dest_file)
                print(f"Copied config: {src_file} -> {dest_file}")

    def _delete_source_files(self, source: str, copied_files: list) -> None:
        files_to_delete = [
            "resume.md",
            "cover_letter.md",
            "job_research.md",
            "profile.md",
            "salary.md",
            "final_review.md"
        ]

        for file_name in copied_files:
            if file_name in files_to_delete:
                try:
                    os.remove(os.path.join(source, file_name))
                    print(f"Deleted: {file_name}")
                except Exception as e:
                    print(f"Failed to delete {file_name}: {e}")


class ConvertCoverLetterToHTMLTool(BaseTool):
    name: str = "convert_cover_letter_to_html"
    description: str = "Converts a cover letter written in Markdown to a modern, single-page A4 HTML format."
    args_schema: Type[BaseModel] = MyCustomToolInput

    def read_markdown_file(self, file_path: str) -> str:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading file '{file_path}': {e}")
                return ""
        else:
            print(f"Warning: The file '{file_path}' was not found.")
            return ""

    def save_html_file(self, html_content: str, output_path: str) -> None:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"Error writing HTML file '{output_path}': {e}")

    def convert_and_save(self, markdown_path: str, html_output_path: str) -> None:
        markdown_content = self.read_markdown_file(markdown_path)

        if markdown_content:
            html_result = self._run(markdown_content)
            self.save_html_file(html_result, html_output_path)
            print(f"HTML successfully saved to '{html_output_path}'")
        else:
            print(f"Skipping conversion. Markdown file '{markdown_path}' not found or empty.")

    def _run(self, argument: str) -> str:
        client = OpenAI(api_key=openai_key)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
You will receive a document in Markdown. Convert it into a single-page A4 HTML.

Instructions:

- Do not alter the cover letter text content.
- Optimize layout, font size, and spacing to ensure it fits one A4 page.
- Use a modern, clean, and professional visual style.
- Maintain strong visual hierarchy (headings, sections).
- Prioritize readability and efficient space usage.
"""
                },
                {
                    "role": "user",
                    "content": argument
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()
