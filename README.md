# Job Application Data Extractor Crew

This project uses **crewAI** to create an intelligent system focused on extracting and structuring detailed information from job postings. It streamlines the initial research phase of the job application process by meticulously analyzing job descriptions and candidate profiles, then synthesizing this data into a standardized format.

## Features

The system comprises specialized agents working collaboratively to achieve a precise, structured output.

### Agents

#### Job Researcher
- **Role**: Analyzes job postings to extract requirements, responsibilities, and company insights.
- **Goal**: Provide comprehensive analysis on job postings to gather all relevant details.

#### Personal Profiler
- **Role**: Analyzes the candidate's professional profile provided.
- **Goal**: Extract key skills, experiences, and achievements from the candidate's background.

#### Profile Match Evaluator
- **Role**: Evaluates the compatibility between the candidate's profile and the job description.
- **Goal**: Provide a compatibility score and actionable feedback on alignment and potential gaps.

#### Output Formatter
- **Role**: Synthesizes and formats all gathered job and candidate compatibility information into a structured JSON object.
- **Goal**: Consolidate all information into a precise JobDetails object, ensuring accurate extraction of work arrangement and specific location, adhering strictly to the Pydantic model.

### Tasks

#### Job Research Task (`job_research_task`)
- **Description**: Analyzes the job posting and generates a detailed report (`job_research.md`).
- **Agent**: Job Researcher

#### Profile Task (`profile_task`)
- **Description**: Analyzes the candidate's profile and generates a report (`profile.md`).
- **Agent**: Personal Profiler

#### Profile Fit Evaluation Task (`evaluate_profile_fit_task`)
- **Description**: Evaluates how well the candidate's profile matches the job requirements, providing a compatibility score and explanation (`profile_fit_evaluation.md`).
- **Agent**: Profile Match Evaluator

#### Format Output Task (`format_output_task`)
- **Description**: Synthesizes all job research, profile analysis, and compatibility score into a single structured JobDetails Pydantic object.
- **Agent**: Output Formatter

## How It Works

The system executes the following tasks sequentially:

1. **Job Analysis**: The Job Researcher extracts detailed information from the provided job URL.
2. **Profile Analysis**: The Personal Profiler analyzes the candidate's `full_profile.md` file.
3. **Profile Fit Evaluation**: The Profile Match Evaluator assesses the match between the analyzed profile and the job requirements, generating a compatibility score.
4. **Data Formatting**: The Output Formatter consolidates all gathered information (job details, candidate profile insights, and compatibility score) into a structured JobDetails JSON object.

The primary output is a compiled JSON file (`job_application_details.json`) containing the structured JobDetails for each processed job URL.

## Installation

**Requirements**: Python >=3.10 <3.13

1. Install UV (a fast Python package manager):
   ```bash
   pip install uv
   ```

2. Install project dependencies:
   ```bash
   crewai install
   ```

3. Configure your Gemini API key in a `.env` file in the project's root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

1. **Prepare your candidate profile**: Place your comprehensive candidate profile in a file named `full_profile.md` in the root of the project.

2. **Define job URLs**: Ensure your job URLs are listed in `src/job_application_crew/job_urls.py`.

3. **Run the system**:
   ```bash
   crewai run
   ```

The results for each processed job will be compiled into `job_application_details.json`.

## Configuration Files

- **`config/agents.yaml`**: Defines the roles, goals, and backstories of each agent.
- **`config/tasks.yaml`**: Defines tasks, their descriptions, expected outputs, and agent assignments.
- **`src/job_application_crew/crew.py`**: Configures the core CrewAI logic, including agent and task definitions, and the JobDetails Pydantic model.
- **`src/job_application_crew/main.py`**: The entry point script that iterates through job URLs and orchestrates the CrewAI execution.
- **`src/job_application_crew/job_urls.py`**: A Python file listing the job URLs to be processed.

## Support

For support or more information:

- [crewAI Documentation](https://docs.crewai.com)
- [crewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Community Discord](https://discord.gg/X4JWnZnxPb)