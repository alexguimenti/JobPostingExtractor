#!/usr/bin/env python
import os
import warnings
import json
import csv # Import the csv module for CSV operations
from urllib.parse import urlparse, urlunparse 

# Ensure these imports align with your project's structure
from job_application_crew.crew import JobApplicationCrew, JobDetails 
from job_application_crew.job_urls import job_urls as raw_job_urls

# Suppress specific warnings from third-party libraries that are not critical
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Define the output file for compiled job details
COMPILED_JOB_DETAILS_FILE = "job_application_details.json"
# Define the output file for CSV
COMPILED_CSV_FILE = "job_applications.csv"

def compile_results(new_job_details: dict, output_file: str = COMPILED_JOB_DETAILS_FILE):
    """
    Reads existing job details from the JSON file, appends the new details,
    and writes the updated list back to the file.
    """
    all_job_details = []
    
    # Attempt to read existing content from the file
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip(): 
                    all_job_details = json.loads(content)
                else:
                    print(f"File '{output_file}' exists but is empty. Starting with an empty list.")
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Could not decode existing JSON in '{output_file}'. "
                  f"The file might be corrupted. Starting with an empty list. Error: {e}")
            all_job_details = [] 
        except Exception as e:
            print(f"⚠️ Warning: Error reading '{output_file}'. Starting with an empty list. Error: {e}")
            all_job_details = []

    # Ensure all_job_details is a list, even if the file contained a single JSON object
    if not isinstance(all_job_details, list):
        print(f"⚠️ Warning: File '{output_file}' does not contain a JSON list. Converting to list and appending.")
        all_job_details = [all_job_details] 

    # Append the new job details
    all_job_details.append(new_job_details)

    # Write the updated list back to the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_job_details, f, indent=2, ensure_ascii=False)
        print(f"💾 Results compiled and saved to '{output_file}'")
    except Exception as e:
        print(f"❌ ERROR saving results to '{output_file}': {e}")

def json_to_csv(json_file_path: str, csv_file_path: str):
    """
    Reads a JSON file containing a list of job details and converts it into a CSV file.
    Each key in the JSON objects becomes a column header in the CSV.
    """
    if not os.path.exists(json_file_path):
        print(f"❌ Error: JSON file not found at '{json_file_path}'. CSV conversion skipped.")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON from '{json_file_path}': {e}. CSV conversion skipped.")
        return
    except Exception as e:
        print(f"❌ An unexpected error occurred while reading '{json_file_path}': {e}. CSV conversion skipped.")
        return

    if not data:
        print(f"⚠️ Warning: JSON file '{json_file_path}' is empty. No CSV will be generated.")
        return
    
    # Ensure data is a list of dictionaries
    if not isinstance(data, list):
        print(f"⚠️ Warning: JSON data is not a list. Attempting to convert a single object.")
        data = [data]

    # Extract all unique keys from all dictionaries to use as CSV headers
    fieldnames = []
    for entry in data:
        for key in entry.keys():
            if key not in fieldnames: # Ensure uniqueness
                fieldnames.append(key)
    
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader() # Write the header row
            writer.writerows(data) # Write all the data rows
        print(f"✅ Successfully converted '{json_file_path}' to '{csv_file_path}'.")
    except Exception as e:
        print(f"❌ Error writing CSV file to '{csv_file_path}': {e}")

def run():
    """
    Main pipeline to execute the CrewAI job application automation.
    For each job URL, run the Crew to generate job details and compile them into a single JSON file.
    After processing all URLs, convert the compiled JSON to a CSV file.
    """
    # --- URL Cleaning ---
    cleaned_job_urls = []
    for url in raw_job_urls:
        parsed_url = urlparse(url)
        # Create a new URL component tuple with an empty query string
        cleaned_url_components = parsed_url._replace(query="")
        # Reconstruct the URL without the query string
        cleaned_url = urlunparse(cleaned_url_components)
        cleaned_job_urls.append(cleaned_url)
    
    total_urls = len(cleaned_job_urls)

    # Process each job URL in the list
    for i, url in enumerate(cleaned_job_urls):
        print(f"\n--- Processing job {i+1}/{total_urls}: {url} ---")
        
        # Create a new Crew instance for each URL to ensure a clean state
        current_crew = JobApplicationCrew().crew()
        
        inputs = {'job_url': url}
        
        try:
            print("🚀 Starting CrewAI pipeline...")
            # kickoff now returns a CrewOutput object
            crew_output = current_crew.kickoff(inputs=inputs)

            # Access the 'raw' or 'result' property of the CrewOutput object.
            # 'raw' is typically the raw data from the last task, 'result' is the final formatted outcome.
            # If you've used output_json=JobDetails, 'raw' should be the dictionary/Pydantic object.
            job_details_data = crew_output.raw 
            
            # Convert the result to a Python dictionary if it's not already one
            if isinstance(job_details_data, JobDetails):
                processed_details_dict = job_details_data.model_dump()
            elif isinstance(job_details_data, dict):
                processed_details_dict = job_details_data
            else:
                # If the return is a JSON string (less common with output_json=Model)
                try:
                    processed_details_dict = json.loads(job_details_data)
                except json.JSONDecodeError:
                    print(f"❌ Error: Crew output is not valid JSON or a JobDetails object for {url}. Output received: {job_details_data}")
                    continue # Skip to the next URL if the output is invalid
            
            print(f"✅ Job analysis complete for: {url}")
            
            # Compile the result into the accumulated JSON file
            compile_results(processed_details_dict, COMPILED_JOB_DETAILS_FILE)
            
        except Exception as e:
            # Log and continue if an error occurs for a specific job URL
            print(f"❌ ERROR: An error occurred while executing the crew for {url}: {e}")
            continue

    print("\n--- All job applications have been processed ---")
    
    # --- Convert compiled JSON to CSV ---
    print(f"\n--- Starting CSV conversion ---")
    json_to_csv(COMPILED_JOB_DETAILS_FILE, COMPILED_CSV_FILE)
    print(f"--- CSV conversion complete ---")

if __name__ == "__main__":
    # Entry point for script execution
    run()