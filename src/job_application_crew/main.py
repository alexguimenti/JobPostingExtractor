#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime

from job_application_crew.crew import JobApplicationCrew
from job_application_crew.tools.custom_tool import (
    BackupMarkdownFilesTool,
    ConvertMarkdownToHTMLTool,
    ConvertCoverLetterToHTMLTool
)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Constants
RESUME_MD_PATH = "resume.md"
RESUME_HTML_PATH = "resume.html"
COVER_LETTER_MD_PATH = "cover_letter.md"
COVER_LETTER_HTML_PATH = "cover_letter.html"

def run():
    """
    Execute the CrewAI pipeline for job application automation.
    
    This function will:
    1. Run the Crew to generate all required files.
    2. Convert the generated resume.md to a modern, single-page HTML (resume.html).
    3. Convert the generated cover_letter.md to a modern, single-page HTML (cover_letter.html).
    4. Backup all generated Markdown (.md) and HTML (.html) files to a structured destination folder.
    """

    inputs = {
        'job_url': 'https://www.happening.xyz/careers/4461918101'
    }

    crew = JobApplicationCrew()
    html_tool = ConvertMarkdownToHTMLTool()
    backup_tool = BackupMarkdownFilesTool()
    cover_letter_tool = ConvertCoverLetterToHTMLTool()


    try:
        print("Running Crew...")
        crew.crew().kickoff(inputs=inputs)

        """
        if os.path.exists(RESUME_MD_PATH):
            print(f"Generating HTML from {RESUME_MD_PATH}...")
            html_tool.convert_and_save(RESUME_MD_PATH, RESUME_HTML_PATH)
        else:
            print(f"Warning: The file '{RESUME_MD_PATH}' was not found. Skipping HTML generation.")

        if os.path.exists(COVER_LETTER_MD_PATH):
            print(f"Generating HTML from {COVER_LETTER_MD_PATH}...")
            cover_letter_tool.convert_and_save(COVER_LETTER_MD_PATH, COVER_LETTER_HTML_PATH)
        else:
            print(f"Warning: The file '{COVER_LETTER_MD_PATH}' was not found. Skipping HTML generation.")
        """

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    print("Running Backup...")
    backup_tool.run()


if __name__ == "__main__":
    run()
