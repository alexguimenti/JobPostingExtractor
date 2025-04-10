#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from job_application_crew.crew import JobApplicationCrew
from job_application_crew.tools.custom_tool import BackupMarkdownFilesTool
from job_application_crew.tools.custom_tool import ConvertMarkdownToHTMLTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # job_url = input("🔗 Paste job URL (ex: LinkedIn): ").strip()

    inputs = {
        'job_url': 'https://www.happening.xyz/careers/4572033101'
    }

    html_tool = ConvertMarkdownToHTMLTool()
    markdown_content = html_tool.read_markdown_file("resume.md")

    try:
        JobApplicationCrew().crew().kickoff(inputs=inputs)
        resume_path = "resume.md"

        if markdown_content:
            try:
                html_tool.convert_and_save("resume.md", "resume.html")

            except Exception as e:
                print(f"Error while processing '{resume_path}': {e}")
        else:
            print(f"Warning: The file '{resume_path}' was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # Use the backup tool
    backup_tool = BackupMarkdownFilesTool()
    backup_tool.run()