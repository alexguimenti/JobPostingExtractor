#!/usr/bin/env python
import sys
import warnings
import os
import shutil
import re

from datetime import datetime

from job_application_crew.crew import JobApplicationCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_url': 'https://www.linkedin.com/jobs/view/4184492958'
    }
    
    try:
        JobApplicationCrew().crew().kickoff(inputs=inputs)
        # Reopen and re-save the file with the correct UTF-8 encoding
        with open("resume.md", "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        


        # (Optional) Fix corrupted characters caused by wrong encoding
        replacements = {
            "â€“": "–",   # en dash
            "â€”": "—",   # em dash
            "â€˜": "‘",   # left single quote
            "â€™": "’",   # right single quote
            "â€œ": "“",   # left double quote
            "â€�": "”",   # right double quote
            "â€¦": "…",   # ellipsis
            "SÃ£o": "São" # common malformed version of 'São'
        }

        for wrong, correct in replacements.items():
            content = content.replace(wrong, correct)

        # Overwrite the file with clean UTF-8 content
        with open("resume.md", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    # backup_markdown_files()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        JobApplicationCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        JobApplicationCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        JobApplicationCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

import os
import shutil
from datetime import datetime
import re

def backup_markdown_files(
    source=r"C:\Users\alexg\Documents\crewai\job_application_crew",
    destination_base=r"D:\Documents\Jobs Application",
    job_research_filename="job_research.md"
):
    # Full path to the job_research.md file
    job_research_path = os.path.join(source, job_research_filename)

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

    # Copy all .md files from source to destination
    copied_files = []
    for file in os.listdir(source):
        if file.endswith(".md"):
            source_path = os.path.join(source, file)
            destination_path = os.path.join(destination, file)
            shutil.copy2(source_path, destination_path)
            copied_files.append(file)
            print(f"Copied: {file}")

    print(f"All .md files have been successfully copied to '{destination}'.")

    # Files to delete after successful copy
    files_to_delete = ["resume.md", "cover_letter.md", "job_research.md", "profile.md", "salary.md"]

    for file_to_delete in files_to_delete:
        if file_to_delete in copied_files:
            try:
                os.remove(os.path.join(source, file_to_delete))
                print(f"Deleted: {file_to_delete}")
            except Exception as e:
                print(f"Failed to delete {file_to_delete}: {e}")
