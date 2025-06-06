import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI

# Load OpenAI API Key from .env
load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Define your Agents

planner = Agent(
    role="Planner",
    goal="Break down user goals into a sequence of learning tasks",
    backstory="You're a productivity and learning expert who helps users plan complex topics into achievable milestones.",
    llm=llm,
    verbose=True
)

researcher = Agent(
    role="Researcher",
    goal="Generate summaries or links to beginner-friendly learning materials for each task",
    backstory="You're a seasoned AI assistant trained on educational and technical content. You provide helpful resources and explanations.",
    llm=llm,
    verbose=True
)

scheduler = Agent(
    role="Scheduler",
    goal="Create a 7-day learning schedule from a task list with logical distribution",
    backstory="You're an expert in time management and learning science. You arrange tasks into a structured weekly schedule.",
    llm=llm,
    verbose=True
)

# Define the user goal
user_goal = "Learn Python for network automation in one week"

# Define tasks

task1 = Task(
    description=f"Break down the goal '{user_goal}' into daily learning tasks for a beginner.",
    expected_output="A list of 7 learning objectives (1 per day) with increasing difficulty.",
    agent=planner
)

task2 = Task(
    description="Generate concise summaries or beginner-level learning resources for each of the daily tasks from task1.",
    expected_output="Detailed content or learning material suggestions for each daily task.",
    agent=researcher,
    depends_on=[task1]
)

task3 = Task(
    description="Create a weekly study plan mapping each task and resource to a specific day.",
    expected_output="A 7-day plan with tasks, estimated study time, and notes.",
    agent=scheduler,
    depends_on=[task2]
)

# Create the Crew
crew = Crew(
    agents=[planner, researcher, scheduler],
    tasks=[task1, task2, task3],
    verbose=True
)

# Run the Crew
final_output = crew.run()
print("\n🎯 Final Weekly Plan:\n")
print(final_output)