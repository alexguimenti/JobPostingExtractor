# Job Application Assistant Crew

This project uses [crewAI](https://crewai.com) to create an intelligent assistance system for job applications, automating and optimizing the process of preparing resumes and cover letters.

## Features

The system consists of several specialized agents working together:

### Agents

1. **Job Researcher**
   - **Role:** Analyzes job postings to extract requirements, responsibilities, and company culture.
   - **Goal:** Provide amazing analysis on job postings to help job applicants.

2. **Personal Profiler**
   - **Role:** Analyzes the candidate's professional profile.
   - **Goal:** Highlight key skills, experiences, and achievements to help candidates stand out.

3. **Profile Match Evaluator**
   - **Role:** Evaluates the fit between the candidate's profile and the job description.
   - **Goal:** Provide a fit score and actionable feedback on alignment and gaps.

4. **Resume Strategist**
   - **Role:** Refines and adapts the resume to match the target job.
   - **Goal:** Make the resume stand out by emphasizing relevant skills and experiences.

5. **Cover Letter Strategist**
   - **Role:** Creates a new, original cover letter tailored to the job and company.
   - **Goal:** Make the cover letter stand out by aligning it with the job requirements and best practices.

6. **Compensation Analyst**
   - **Role:** Provides realistic salary expectations based on the role's location and company.
   - **Goal:** Suggest fair compensation ranges using market data and benchmarks.

7. **Final Application Reviewer**
   - **Role:** Reviews all application materials for alignment, coherence, and impact.
   - **Goal:** Ensure all documents are consistent, professional, and optimized for submission.

---

### Tasks

1. **Job Research Task** (`job_research_task`)
   - Analyzes the job posting and generates a detailed report (`job_research.md`).

2. **Profile Task** (`profile_task`)
   - Analyzes the candidate's profile and generates a report (`profile.md`).

3. **Profile Fit Evaluation Task** (`evaluate_profile_fit_task`)
   - Evaluates how well the candidate's profile matches the job requirements, providing a fit score and explanation.

4. **Resume Strategy Task** (`resume_strategy_task`)
   - Adapts the resume to the job, ensuring alignment with requirements and guidelines. Outputs `resume.md`.

5. **Cover Letter Strategy Task** (`cover_letter_strategy_task`)
   - Creates a new, fully customized cover letter based on the job and candidate profile. Outputs `cover_letter.md`.

6. **Compensation Analysis Task** (`compensation_analysis_task`)
   - Provides a realistic compensation range for the role, tailored to the company and location. Outputs `salary.md`.

7. **Final Review Task** (`final_review_task`)
   - Reviews all application documents for alignment, consistency, and readiness. Outputs `final_review.md`.

---

## How It Works

The system executes the following tasks sequentially (or as configured):

1. **Job Analysis**: Extracts detailed information from the job posting.
2. **Profile Analysis**: Analyzes the candidate's complete profile.
3. **Profile Fit Evaluation**: Assesses the match between profile and job.
4. **Resume Optimization**: Adapts the resume based on previous analyses.
5. **Cover Letter Creation**: Develops a personalized letter for the job.
6. **Compensation Analysis**: Suggests a fair salary range for the role.
7. **Final Review**: Ensures all documents are aligned and ready for submission.

Each task generates a specific output file (e.g., `job_research.md`, `profile.md`, `resume.md`, `cover_letter.md`, `salary.md`, `final_review.md`).

## Installation

Requirements: Python >=3.10 <3.13

1. Install UV (dependency manager):
```bash
pip install uv
```

2. Install project dependencies:
```bash
crewai install
```

3. Configure your OpenAI API key in the `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## Usage

1. Place your complete profile in `full_profile.md`
2. Add your current resume in `original_resume.md`
3. Add your base cover letter in `original_cover_letter.md`
4. Run the system with:
```bash
crewai run
```

## Configuration Files

- `config/agents.yaml`: Defines the roles and goals of each agent
- `config/tasks.yaml`: Defines tasks and their expected outputs
- `src/job_application_crew/crew.py`: Configures agent logic and tools
- `src/job_application_crew/main.py`: Defines required inputs for execution

## Support

For support or more information:
- [crewAI Documentation](https://docs.crewai.com)
- [crewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Community Discord](https://discord.com/invite/X4JWnZnxPb)
