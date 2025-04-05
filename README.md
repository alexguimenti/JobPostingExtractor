# Job Application Assistant Crew

This project uses [crewAI](https://crewai.com) to create an intelligent assistance system for job applications, automating and optimizing the process of preparing resumes and cover letters.

## Features

The system consists of four specialized agents working together:

1. **Job Researcher**: Thoroughly analyzes the job posting, extracting crucial information about requirements, responsibilities, and company culture.

2. **Profiler**: Analyzes the candidate's professional profile to identify strengths and relevant experiences.

3. **Resume Strategist**: Adapts the candidate's resume to better align with job requirements while maintaining truthful information from the profile.

4. **Cover Letter Strategist**: Personalizes the cover letter to highlight the candidate's most relevant qualifications for the specific position.

## How It Works

The system executes the following tasks sequentially:

1. Job Analysis (job_research_task):
   - Extracts detailed information from the job posting
   - Identifies technical and soft skill requirements
   - Analyzes company culture
   - Generates a complete report in `job_research.md`

2. Profile Analysis (profile_task):
   - Analyzes the candidate's complete profile
   - Identifies strengths and relevant experiences
   - Generates a report in `profile.md`

3. Resume Optimization (resume_strategy_task):
   - Adapts the resume based on previous analyses
   - Maintains all truthful information
   - Generates an optimized version in `resume.md`

4. Cover Letter Creation (cover_letter_strategy_task):
   - Develops a personalized letter
   - Aligns the narrative with the job and company
   - Generates the result in `cover_letter.md`

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
