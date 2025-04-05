from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task


from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  SerperDevTool
)

manager_llm = LLM(model="gpt-4")


search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_full_profile = FileReadTool(file_path='./full_profile.md')
read_resume = FileReadTool(file_path='./original_resume.md')
read_resume_guide = FileReadTool(file_path='./resume_guide.md')
read_cover_letter = FileReadTool(file_path='./original_cover_letter.md')
read_cover_letter_guide = FileReadTool(file_path='./cover_letter_guide.md')


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class JobApplicationCrew():
    """JobApplicationCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    # @agent
    # def researcher(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['researcher'],
    #         verbose=True
    #     )

    @agent
    def job_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['job_researcher'],
            tools=[search_tool, scrape_tool],
            verbose=True
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['profiler'],
            tools=[search_tool, scrape_tool, read_full_profile],
            verbose=True,
        )
    
    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_strategist'],
            tools=[read_resume, read_resume_guide],
            verbose=True
        )

    @agent
    def cover_letter_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['cover_letter_strategist'],
            tools=[read_cover_letter, read_cover_letter_guide],
            verbose=True
        )

    # @agent
    # def reporting_analyst(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['reporting_analyst'],
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    # @task
    # def research_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['research_task'],
    #     )

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'],
    #         output_file='report.md'
    #     )
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
            #depends_on=['profile_task'] 
        )
    
    @task
    def cover_letter_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['cover_letter_strategy_task'],
            output_file='cover_letter.md',
            #depends_on=['profile_task'] 
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the JobApplicationCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            manager_llm=manager_llm,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
