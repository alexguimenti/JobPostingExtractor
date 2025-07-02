import os
import warnings
from datetime import datetime
from typing import Optional # Correctly importing Optional from typing

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel, Field, field_serializer # All Pydantic imports in one line

# Suppress specific warnings from third-party libraries that might use deprecated Pydantic features
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

# --- Model Definition ---
class JobDetails(BaseModel):
    """
    Model to hold job details extracted from a job posting.
    """
    company_name: str = Field(..., description="Name of the company offering the job.")
    job_title: str = Field(..., description="Title of the job position.")
    job_description: str = Field(..., description="Detailed description of the job responsibilities and requirements.")
    
    work_arrangement: str = Field(..., description="Type of work arrangement, one of: 'Remote', 'Hybrid', 'On-site'.")
    
    specific_location: str = Field(..., description="The primary geographic location associated with the job or the company's headquarters (e.g., 'São Paulo, Brazil', 'Seattle, WA, USA'). Even for 'Remote' roles, provide the company's main location or the base country if specified. If absolutely no location can be inferred, state 'Not specified'.")
    salary_range: Optional[str] = Field(None, description="Salary range for the job, if available. Format: 'min-max' (e.g., '50000-70000'). If not specified, this field can be None.")
    compatibility_score: int = Field(..., description="Score indicating how well the candidate's profile matches the job requirements (1-5).")
    date_posted: str = Field(..., description="Date when the job was posted, in 'YYYY-MM-DD' format.")
    current_date: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Current date for reference (ISO 8601 format).")
    requires_other_languages: bool = Field(
        ..., 
        description="Boolean indicating if the job requires proficiency in a language other than English or Spanish (e.g., German, Dutch, French, etc.)."
    )
    link: str = Field(..., description="Link to the job posting for reference.")

    # Ensures current_date is always an ISO 8601 string when serialized
    @field_serializer('current_date')
    def serialize_dt(self, dt: datetime) -> str:
        # Check if it's a datetime object (in case it's already a string)
        if isinstance(dt, datetime):
            return dt.isoformat()
        return dt # If it's already a string, return as is


# --- LLM Configuration ---
# It's good practice to define the LLM here so all agents use the same one by default,
# or so you can easily inject it.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_llm = LLM(
    model='gemini/gemini-pro', # Use 'gemini-pro' to start, 'gemini-2.5-pro' might be more expensive/restricted
    api_key=GEMINI_API_KEY,
    temperature=0.3 # A bit lower for more consistent results
)

# --- Tool Initialization ---
# Global tools for agents to use
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# File readers for specific input files (passed to agents that need them)
# Keep paths relative to the execution directory, or use absolute paths if necessary.
read_full_profile = FileReadTool(file_path='./full_profile.md')
# The following FileReadTools were defined but not used in the provided agent/task definitions.
# If you plan to use them in other agents/tasks, keep them. Otherwise, they can be removed.
# read_resume = FileReadTool(file_path='./original_resume.md')
# read_resume_guide = FileReadTool(file_path='./resume_guide.md')
# read_cover_letter_guide = FileReadTool(file_path='./cover_letter_guide.md')


@CrewBase
class JobApplicationCrew:
    """
    Main CrewAI class that defines all agents and tasks for the job application pipeline.
    Each agent is responsible for a specific part of the process, and tasks are mapped to outputs.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize the LLM for the crew and agents
        self.llm = gemini_llm

    # --- Agent Definitions ---
    @agent
    def researcher(self) -> Agent:
        """Agent responsible for job posting research and extraction."""
        return Agent(
            config=self.agents_config['researcher'],
            tools=[scrape_tool, search_tool], # search_tool can be useful for more context
            allow_delegation=False,
            verbose=True,
            #llm=self.llm # Pass the LLM to the agent
        )

    @agent
    def profiler(self) -> Agent:
        """Agent responsible for analyzing the candidate's profile."""
        return Agent(
            config=self.agents_config['profiler'],
            tools=[read_full_profile], # Only the necessary tool
            allow_delegation=False,
            verbose=True,
            #llm=self.llm # Pass the LLM to the agent
        )

    @agent
    def evaluator(self) -> Agent:
        """Agent that evaluates the fit between profile and job requirements."""
        return Agent(
            config=self.agents_config['evaluator'],
            allow_delegation=False,
            verbose=True,
            #llm=self.llm # Pass the LLM to the agent
        )

    @agent
    def output_formatter(self) -> Agent:
        """Agent that synthesizes and formats a single JobDetails JSON object."""
        return Agent(
            config=self.agents_config['output_formatter'],
            # The output_formatter agent does NOT need file read/write tools here
            # because file manipulation will be handled externally by the main script.
            allow_delegation=False,
            verbose=True,
            #llm=self.llm # Pass the LLM to the agent
        )

    # --- Task Definitions ---
    @task
    def job_research_task(self) -> Task:
        """Task: Analyze job posting and generate job research report."""
        return Task(
            config=self.tasks_config['job_research_task'],
            output_file='job_research.md',
            agent=self.researcher()
        )

    @task
    def profile_task(self) -> Task:
        """Task: Analyze candidate profile and generate profile report."""
        return Task(
            config=self.tasks_config['profile_task'],
            output_file='profile.md',
            agent=self.profiler()
        )

    @task
    def evaluate_profile_fit_task(self) -> Task:
        """Task: Evaluate profile-to-job fit and generate evaluation report."""
        return Task(
            config=self.tasks_config['evaluate_profile_fit_task'],
            context=[self.job_research_task(), self.profile_task()],
            output_file='profile_fit_evaluation.md',
            agent=self.evaluator()
        )

    @task
    def format_output_task(self) -> Task:
        """
        Task: Synthesize all job research, profile analysis, and compatibility score
        into a single structured JobDetails Pydantic object.
        """
        return Task(
            config=self.tasks_config['format_output_task'],
            context=[self.job_research_task(), self.profile_task(), self.evaluate_profile_fit_task()],
            output_json=JobDetails, # This instructs the agent to produce a JobDetails object
            # We don't need output_file here, as the result will be returned directly by crew.kickoff()
            agent=self.output_formatter()
        )

    # --- Crew Definition ---
    @crew
    def crew(self) -> Crew:
        """
        Creates and returns the Crew instance with all agents and tasks.
        Uses the configured LLM for all agents.
        """
        return Crew(
            agents=[
                self.researcher(),
                self.profiler(),
                self.evaluator(),
                self.output_formatter()
            ],
            tasks=[
                self.job_research_task(),
                self.profile_task(),
                self.evaluate_profile_fit_task(),
                self.format_output_task()
            ],
            process=Process.sequential,
            verbose=True,
            #llm=self.llm # Pass the LLM to the Crew
        )