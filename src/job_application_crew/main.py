#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime

from job_application_crew.crew import JobApplicationCrew
from job_application_crew.tools.custom_tool import (
    BackupMarkdownFilesTool,
    ConvertMarkdownToHTMLTool
)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Constants
RESUME_MD_PATH = "resume.md"
RESUME_HTML_PATH = "resume.html"

def run():
    """
    Execute the CrewAI pipeline for job application automation.
    This function will:
    1. Run the Crew.
    2. Convert the generated resume.md to HTML.
    3. Backup all generated markdown and HTML files.
    """

    inputs = {
        'job_url': 'https://www.happening.xyz/careers/4572033101'
    }

    crew = JobApplicationCrew()
    html_tool = ConvertMarkdownToHTMLTool()
    backup_tool = BackupMarkdownFilesTool()

    try:
        print("Running Crew...")
        #crew.crew().kickoff(inputs=inputs)

        if os.path.exists(RESUME_MD_PATH):
            print(f"Generating HTML from {RESUME_MD_PATH}...")
            html_tool.convert_and_save(RESUME_MD_PATH, RESUME_HTML_PATH)
        else:
            print(f"Warning: The file '{RESUME_MD_PATH}' was not found. Skipping HTML generation.")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    print("Running Backup...")
    #backup_tool.run()


if __name__ == "__main__":
    run()
