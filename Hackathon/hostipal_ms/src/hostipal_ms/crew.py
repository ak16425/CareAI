from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool, FileReadTool
load_dotenv()

@CrewBase
class HostipalMs():
	"""HostipalMs crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	@agent
	def website_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['website_scraper'],
			tools=[ScrapeWebsiteTool(website_url="https://kdhospital.co.in/doctors")],
			verbose=True
		)

	@agent
	def specialist_recommender(self) -> Agent:
		return Agent(
			config=self.agents_config['specialist_recommender'],
			verbose=True,
			allow_delegation=False,
		)
	@agent
	def appointment_scheduler(self) -> Agent:
		return Agent(
			config=self.agents_config['appointment_scheduler'],
			verbose=True,
			allow_delegation=False,
		)
  
	@agent
	def admission_officer(self) -> Agent:
		return Agent(
			config=self.agents_config['admission_officer'],
			verbose=True,
			allow_delegation=False,
		)
  
	@agent
	def billing_officer(self) -> Agent:
		return Agent(
			config=self.agents_config['billing_officer'],
			verbose=True,
			allow_delegation=False,
		)

	@task
	def website_scrape_task(self) -> Task:
		return Task(
			config=self.tasks_config['website_scrape_task'],
			output_file='report.md'
		)
	
	@task
	def recommend_specialist(self) -> Task:
		return Task(
			config=self.tasks_config['recommend_specialist'],
   			human_input=True,
		)
  
	@task
	def schedule_appointment(self) -> Task:
		return Task(
			config=self.tasks_config['schedule_appointment'],

		)
  
	@task
	def admit_patient(self) -> Task:
		return Task(
			config=self.tasks_config['admit_patient']
		)
  
	@task
	def process_billing(self) -> Task:
		return Task(
			config=self.tasks_config['process_billing'],
		)

	@crew
	def opd_crew(self) -> Crew:
		"""Creates the HostipalMs crew"""
		return Crew(
			agents=[self.website_scraper(), self.specialist_recommender(), self.appointment_scheduler() ], # Automatically created by the @agent decorator
			tasks=[self.website_scrape_task(), self.recommend_specialist(), self.schedule_appointment()], # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
  
	@crew
	def admit_crew(self) -> Crew:
		"""Creates the HostipalMs crew"""
		return Crew(
			agents=[self.admission_officer()],
			tasks=[self.admit_patient()], 
			process=Process.sequential,
			verbose=True,
		
		)
  
	@crew
	def bill_crew(self) -> Crew:
		"""Creates the HostipalMs crew"""
		return Crew(
			agents=[self.billing_officer()],
			tasks=[self.process_billing()], 
			process=Process.sequential,
			verbose=True,
		
		)
