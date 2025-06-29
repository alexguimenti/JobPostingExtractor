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
from job_application_crew.job_urls import job_urls

# Suppress specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# --- GLOBAL CONFIGURATION ---
# Set this to True if you want to generate HTML files after each crew run, False otherwise.
GENERATE_HTML_FILES = False

# Constants for file paths
RESUME_MD_PATH = "resume.md"
RESUME_HTML_PATH = "resume.html"
COVER_LETTER_MD_PATH = "cover_letter.md"
COVER_LETTER_HTML_PATH = "cover_letter.html"

def generate_and_save_html(url, html_tool, cover_letter_tool):
    """
    Generates HTML files from Markdown resume and cover letter.

    Args:
        url (str): The URL of the job being processed (for logging purposes).
        html_tool: An instance of ConvertMarkdownToHTMLTool.
        cover_letter_tool: An instance of ConvertCoverLetterToHTMLTool.
    """
    if os.path.exists(RESUME_MD_PATH):
        print(f"Generating HTML from {RESUME_MD_PATH}...")
        html_tool.convert_and_save(RESUME_MD_PATH, RESUME_HTML_PATH)
    else:
        print(f"Warning: The file '{RESUME_MD_PATH}' was not found. Skipping HTML generation for {url}.")

    if os.path.exists(COVER_LETTER_MD_PATH):
        print(f"Generating HTML from {COVER_LETTER_MD_PATH}...")
        cover_letter_tool.convert_and_save(COVER_LETTER_MD_PATH, COVER_LETTER_HTML_PATH)
    else:
        print(f"Warning: The file '{COVER_LETTER_MD_PATH}' was not found. Skipping HTML generation for {url}.")


def run():
    """
    Executes the CrewAI pipeline for job application automation.

    This function will:
    1. Run the Crew to generate all required files for each job URL provided.
    2. Optionally, convert the generated resume.md and cover_letter.md to HTML.
    3. Backup all generated Markdown (.md) and HTML (.html) files to a structured destination folder.
    """

    # List of job URLs to process
    # job_urls = [
    #     'https://job-boards.greenhouse.io/truveta/jobs/5563344004'
    #     'https://jobs.gem.com/nutrislice/am9icG9zdDq-Vjz3z4iPR98Qh_HAkkkC?applicant_guid=8fbdeee7-6283-44d8-9266-77cffa020d83&source=JobTarget%20via%20LinkedIn%20Limited%20Listing%20Organic&utm_source=JobTarget&utm_medium=LinkedIn%20Limited%20Listing%20Organic&utm_campaign=Technical%20Product%20Manager%20(am9icG9zdDq-Vjz3z4iPR98Qh_HAkkkC)&_jtochash=4GaBkMSYXwGOltY2DtYq4m&_jtocprof=GwkDSO88TjrEDfKVofIbiqqfJ5DetJKY'
    # ]

    crew = JobApplicationCrew()
    html_tool = ConvertMarkdownToHTMLTool()
    backup_tool = BackupMarkdownFilesTool()
    cover_letter_tool = ConvertCoverLetterToHTMLTool()

    total_urls = len(job_urls)

    for i, url in enumerate(job_urls):
        # Progress log: Displaying current URL being processed and overall progress
        print(f"\n--- Processing job {i+1}/{total_urls}: {url} ---")
        
        inputs = {
            'job_url': url
        }

        try:
            print("Running Crew...")
            crew.crew().kickoff(inputs=inputs)

            # --- Conditional HTML Generation ---
            if GENERATE_HTML_FILES:
                generate_and_save_html(url, html_tool, cover_letter_tool)
            else:
                print("HTML file generation is disabled by GENERATE_HTML_FILES setting.")

            # Moving the backup inside the loop to occur after each URL is processed
            # It's crucial that your 'BackupMarkdownFilesTool' handles unique file names
            # for each job (e.g., by adding a timestamp or job ID),
            # otherwise, files generated from previous jobs will be overwritten,
            # and only the last run's files will be kept in the backup.
            print("Running Backup for current URL's files...")
            backup_tool.run()

        except Exception as e:
            print(f"ERROR: An error occurred while running the crew for {url}: {e}")
            # Continue to the next URL even if one fails
            continue

    print("\n--- All job applications processed ---")


if __name__ == "__main__":
    run()