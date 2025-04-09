#!/usr/bin/env python
import sys
import warnings
import os
import shutil
import re

from datetime import datetime

from job_application_crew.crew import JobApplicationCrew
from job_application_crew.tools.custom_tool import BackupMarkdownFilesTool

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
        'job_url': 'https://www.linkedin.com/jobs/view/4104765323'
    }
    
    try:
        JobApplicationCrew().crew().kickoff(inputs=inputs)
        # Reopen and re-save the file with the correct UTF-8 encoding
        with open("resume.md", "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Overwrite the file with clean UTF-8 content
        with open("resume.md", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    # Use the backup tool
    backup_tool = BackupMarkdownFilesTool()
    backup_tool.run()


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
