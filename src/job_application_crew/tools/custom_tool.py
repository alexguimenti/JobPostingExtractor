from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import shutil
from datetime import datetime
import re
from openai import OpenAI
import sys
from dotenv import load_dotenv

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


class ConvertMarkdownToHTMLTool(BaseTool):
    name: str = "convert_markdown_to_html"
    description: str = "Converts a resume written in Markdown to a modern, single-page A4 HTML format using a predefined template."
    args_schema: Type[BaseModel] = MyCustomToolInput  # seu schema de entrada

    def _run(self, argument: str) -> str:
        client = OpenAI(api_key=openai_key)  # coloque aqui sua chave real

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You will receive a resume in Markdown. Convert it into a single-page A4 HTML using the provided HTML structure and styles.
                    
                    Instructions:

- Do not alter the resume text content.
- Optimize layout, font size, and spacing to ensure it fits one A4 page.
- Use a modern, clean, and professional visual style.
- Maintain strong visual hierarchy (headings, sections).
- Prioritize readability and efficient space usage.

Use this HTML template and styling:


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Alexandre Guimenti - Resume</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Roboto', sans-serif; }
    body { font-size: 10pt; line-height: 1.2; color: #333; margin: 15px; max-width: 210mm; min-height: 297mm; }
    .header { text-align: center; margin-bottom: 8px; }
    h1 { font-size: 20pt; font-weight: 700; margin-bottom: 4px; color: #1a1a1a; }
    .contact-info { font-size: 9pt; margin-bottom: 4px; }
    .divider { height: 1px; background-color: #ddd; margin: 4px 0; }
    h2 { font-size: 12pt; font-weight: 500; color: #1a1a1a; margin-top: 6px; margin-bottom: 4px; border-bottom: 1px solid #ddd; padding-bottom: 2px; }
    .section { margin-bottom: 8px; }
    .job-title, .job-company { font-weight: 700; margin-bottom: 0; }
    .job-period { font-style: italic; font-size: 9pt; margin-bottom: 2px; color: #555; }
    ul { padding-left: 18px; margin: 2px 0 4px 0; }
    li { margin-bottom: 2px; }
    .skills-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .skill-category { font-weight: 700; }
    .skill-items { font-size: 9pt; }
    .two-column { display: flex; gap: 20px; }
    .column { flex: 1; }
    .education-institution { font-weight: 700; }
    .education-detail { font-style: italic; font-size: 9pt; }
    .education-note { font-size: 9pt; color: #555; }
    .personal { font-size: 9pt; }
    .certifications-note { font-style: italic; font-size: 9pt; margin-bottom: 3px; }
    .certifications { font-size: 9pt; }
    a { color: #0066cc; text-decoration: none; }
    p { margin-bottom: 4px; font-size: 9.5pt; text-align: justify; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Alexandre Guimenti</h1>
    <div class="contact-info">
      <strong>Location:</strong> São Paulo, Brazil, Brazil, actively pursuing opportunities abroad and open to relocating. |
      <strong>Email:</strong> alexguimenti@gmail.com |
      <strong>Phone:</strong> +55 12 98168-8627 |
      <strong>LinkedIn:</strong> <a href="https://linkedin.com/in/alexandre-guimenti">linkedin.com/in/alexandre-guimenti</a>
    </div>
  </div>

  <div class="section">
    <h2>Professional Summary</h2>
    <p>Data-driven Product Manager with over 6 years of experience... aligned with company goals.</p>
  </div>

  <div class="section">
    <h2>Skills</h2>
    <div class="skills-grid">
      <div><span class="skill-category">Product & Data:</span> <span class="skill-items">...</span></div>
      <div><span class="skill-category">Technical Skills:</span> <span class="skill-items">...</span></div>
      <div><span class="skill-category">Methodologies:</span> <span class="skill-items">...</span></div>
    </div>
  </div>

  <div class="section">
    <h2>Professional Experience</h2>
    <div class="job"><div class="job-company">AB InBev – BEES</div><div class="job-title">Data Product Manager</div><div class="job-period">Apr. 2024 – Present</div><ul><li>Lead data tracking initiatives...</li></ul></div>
    <div class="job"><div class="job-company">AB InBev – BEES</div><div class="job-title">Product Manager</div><div class="job-period">Sep. 2021 – Mar. 2024</div><ul><li>Led Earning & Challenges...</li></ul></div>
    <div class="job"><div class="job-company">Linx</div><div class="job-title">Product Manager</div><div class="job-period">Dec. 2020 – Sep. 2021</div><ul><li>Managed development...</li></ul></div>
    <div class="job"><div class="job-company">Social Miner</div><div class="job-title">Product Manager</div><div class="job-period">Oct. 2019 – Nov. 2020</div><ul><li>Sole PM reporting directly to CEO...</li></ul></div>
  </div>

  <div class="two-column">
    <div class="column section">
      <h2>Education</h2>
      <div class="education-institution">University of São Paulo (USP)</div>
      <div class="education-detail">B.Sc. in Mechanical Engineering</div>
      <div class="education-note">Top university in Latin America</div>
    </div>
    <div class="column section">
      <h2>Languages</h2>
      <p>Portuguese (Native); English (Advanced); Spanish (Advanced)</p>
    </div>
  </div>

  <div class="section">
    <h2>Certifications</h2>
    <div class="certifications-note">Selected certifications from a portfolio of 40+:</div>
    <p class="certifications">Product Management for AI; Microsoft Power BI; Amplitude Practitioner; Data Analytics; Statistics for Data Science; Deep Learning A-Z; CS50x: Harvard.</p>
  </div>

  <div class="section">
    <div class="personal">
      <strong>Personal Interests:</strong> Running; Music; Games; Reading.
    </div>
  </div>
</body>
</html>
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
        files_to_delete = ["resume.md", "cover_letter.md", "job_research.md", "profile.md", "salary.md", "final_review.md"]

        for file_to_delete in files_to_delete:
            if file_to_delete in copied_files:
                try:
                    os.remove(os.path.join(source, file_to_delete))
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Failed to delete {file_to_delete}: {e}")

        return result_message