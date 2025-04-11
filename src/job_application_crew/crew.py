from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, ScrapeWebsiteTool, SerperDevTool, MDXSearchTool

# Tools Initialization
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
file_read_tool = FileReadTool(diretory='./')

# File Readers
read_full_profile = FileReadTool(file_path='./full_profile.md')
read_resume = FileReadTool(file_path='./original_resume.md')
read_resume_guide = FileReadTool(file_path='./resume_guide.md')
read_cover_letter_guide = FileReadTool(file_path='./cover_letter_guide.md')

# Semantic Search
semantic_search_full_profile = MDXSearchTool(mdx='./full_profile.md')
semantic_search_original_resume = MDXSearchTool(mdx='./original_resume.md')
semantic_search_resume_guide = MDXSearchTool(mdx='./resume_guide.md')
semantic_search_cover_letter_guide = MDXSearchTool(mdx='./cover_letter_guide.md')


#llm=llm(model="ollama/llama3.1:latest", base_url="http://localhost:11434")


@CrewBase
class JobApplicationCrew():
    """Defines the Job Application Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[search_tool, scrape_tool],
            allow_delegation=False,
            #llm=llm,
            verbose=True
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['profiler'],
            tools=[search_tool, scrape_tool, file_read_tool, read_full_profile, semantic_search_full_profile],
            allow_delegation=False,
            #llm=llm,
            verbose=True,
        )
    
    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_strategist'],
            tools=[
                file_read_tool,
                read_full_profile,
                read_resume,
                read_resume_guide,
                semantic_search_full_profile,
                semantic_search_original_resume,
                semantic_search_resume_guide
            ],
            allow_delegation=True,
            #llm=llm,
            verbose=True
        )

    @agent
    def cover_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['cover_strategist'],
            tools=[
                file_read_tool,
                read_cover_letter_guide,
                semantic_search_cover_letter_guide
            ],
            allow_delegation=True,
            #llm=llm,
            verbose=True
        )
    
    @agent
    def compensation_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['compensation_analyst'],
            tools=[file_read_tool],
            allow_delegation=False,
            #llm=llm,
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            tools=[search_tool, scrape_tool, file_read_tool],
            allow_delegation=False,
            #llm=llm,
            verbose=True
        )

    @task
    def job_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_research_task'],
            output_file='job_research.md'
        )

    @task
    def profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['profile_task'],
            #depends_on=['job_research_task'],
            output_file='profile.md'
        )
    
    @task
    def resume_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['resume_strategy_task'],
            output_file='resume.md',
            #async_execution=True,
            #context=['job_research_task', 'profile_task']
            #depends_on=['profile_task'] 
        )
    
    @task
    def cover_letter_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['cover_letter_strategy_task'],
            output_file='cover_letter.md',
            #context=['job_research_task', 'profile_task']
            #async_execution=True,
            #depends_on=['profile_task'] 
        )
    
    @task
    def compensation_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['compensation_analysis_task'],
            output_file='salary.md',
            #async_execution=True,
            #depends_on=['profile_task'] 
        )
    
    @task
    def profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['profile_task'],
            #depends_on=['job_research_task'],
            output_file='profile.md'
        )
    
    @task
    def final_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_review_task'],
            output_file='final_review.md',
            # depends_on=[
            #     'job_research_task',
            #     'profile_task',
            #     'resume_strategy_task',
            #     'cover_letter_strategy_task',
            #     'compensation_analysis_task'
            # ]
        )

    
# CREW DEFINITION
    @crew
    def crew(self) -> Crew:
        """Creates and returns the Crew instance"""
        return Crew(
            #agents=self.agents, # Automatically created by the @agent decorator
            #tasks=self.tasks, # Automatically created by the @task decorator
            agents=[
                self.researcher(),
                self.profiler(),
                self.resume_strategist(),
                self.cover_strategist(),
                self.compensation_analyst(),
                # self.reviewer()
            ],
            tasks=[
                self.job_research_task(),
                self.profile_task(),
                self.resume_strategy_task(),
                self.cover_letter_strategy_task(),
                self.compensation_analysis_task(),
                # self.final_review_task()
            ],
            process=Process.sequential,
            verbose=True,
            # memory=True,
            # short_term_memory=ShortTermMemory(
            #     storage=RAGStorage(
            #         embedder_config={
            #             "provider": "openai",
            #             "config": {"model": 'text-embedding-3-small'}
            #         },
            #         type="short_term",
            #         path="/my_crew1/"
            #     )
            # )
            
        )