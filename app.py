from flask import Flask
from crewai import Agent, Task, Crew, Process
import os

app = Flask(__name__)


researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="You work at a leading tech think tank. Your expertise lies in identifying emerging trends. You have a knack for dissecting complex data and presenting actionable insights.",
    verbose=True,
    allow_delegation=False,
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="You are a renowned Content Strategist, known for your insightful and engaging articles. You transform complex concepts into compelling narratives.",
    verbose=True,
    allow_delegation=True
)


# Research task
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 2 paragraphs long report on the latest AI trends.',
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  agent=writer,
)



@app.route('/run_agents', methods=['GET'])
def run_agents():
    print('Running agents...')
    crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, write_task],
            process=Process.sequential,  # Optional: Sequential task execution is default
            memory=True,
            cache=True,
            max_rpm=5,
        )

    result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
    return result, 200


if __name__ == '__main__':
    app.run(debug=True)
