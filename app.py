import os
from dotenv import load_dotenv
from flask import Flask, request
from crewai import Agent, Task, Crew
from typing import List
from pydantic import BaseModel

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


class CategoryMapping(BaseModel):
    categoryId: str
    transactionId: str

class CategoryMappingList(BaseModel):
    mappings: List[CategoryMapping]

app = Flask(__name__)

categorizer = Agent(
    role='Senior Transaction Categorizer',
    goal='Categorize transactions with predefined categories',
    backstory="You work at a big accounting company and trained to understand and categorize financial transactions. You analyze transaction details like description, merchant name, debit/credit and categorize them into predefined categories.",
    allow_delegation=False,
)

verifier = Agent(
    role='Senior Transaction Verifier',
    goal='Verify the categories of transactions',
    backstory="You work at a big accounting firm and trained to verify the categories of financial transactions. You cross-check the categorized transactions and ensure their accuracy.",
    allow_delegation=True,
)

categorize_task = Task(
    description="Categorize the given transaction: {transactions} based on its details into one of the predefined list of categories: {categories}",
    expected_output='JSON object containing the transaction details and its category.',
    agent=categorizer,
)

verify_task = Task(
    description="Verify the category of the given transaction: {transactions} based on its details. If the category is incorrect, correct it. The possible categories are {categories}.",
    output_json=CategoryMappingList,
    expected_output='A verified JSON object containing the transactionId, and the corrected categoryId',
    agent=verifier,
)

@app.route('/categorize', methods=['POST'])
def run_agents():
    print('Running agents...')

    data = request.get_json(force=True)

    crew = Crew(
            agents=[categorizer, verifier],
            tasks=[categorize_task, verify_task],
            memory=True,
            cache=True,
            max_rpm=100,
        )

    result = crew.kickoff(inputs={"transactions": data['transactions'], 'categories':data['categories']})
    return result, 200



if __name__ == '__main__':
    app.run(port=7777)
