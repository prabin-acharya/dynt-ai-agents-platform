import os
from dotenv import load_dotenv
import agentops
from flask import Flask, request
from crewai import Agent, Task, Crew, Process
from typing import List, Optional
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize AgentOps with your API key from .env
agentops.init()

# Set up OpenAI environment variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'

class CategoryMapping(BaseModel):
    transactionId: str
    categoryId: Optional[str] = None
    subCategoryId: Optional[str] = None

class CategoryMappingList(BaseModel):
    mappings: List[CategoryMapping]

app = Flask(__name__)

@agentops.track_agent(name='transaction-categorizer')
class TransactionCategorizer(Agent):
    def __init__(self):
        super().__init__(
            role='Senior Transaction Categorizer',
            goal='Categorize transactions with predefined categories and subcategories',
            backstory="You work at a big accounting company and trained to understand and categorize financial transactions. You analyze transaction details like description, merchant name, debit/credit and categorize them into predefined categories and subcategories",
            allow_delegation=False,
        )

@agentops.track_agent(name='transaction-verifier')
class TransactionVerifier(Agent):
    def __init__(self):
        super().__init__(
            role='Senior Transaction Verifier',
            goal='Verify the categories and subcategories of transactions',
            backstory="You work at a big accounting firm and trained to verify the categories and subcategories of financial transactions. You cross-check the categorized transactions and ensure their accuracy.",
            allow_delegation=True,
        )

categorizer = TransactionCategorizer()
verifier = TransactionVerifier()

@agentops.record_function('categorize_transactions')
def categorize_task(agent, transactions, categories):
    task = Task(
        description=f"Categorize the given transactions: {transactions} based on their details into one of the predefined list of categories and subcategories: {categories}, remember a subcategory can only be assigned if the parent category is assigned to that transaction.",
        expected_output='JSON object containing the transaction details and its category and subcategory (if applicable).',
        agent=agent,
    )
    return task.execute()

@agentops.record_function('verify_transactions')
def verify_task(agent, transactions, categories):
    task = Task(
        description=f"Verify the category of the given transactions: {transactions} based on their details. If the category and/or subcategory is incorrect, correct it. The possible categories are {categories}. Remember a subcategory can only be assigned if the parent category is assigned added to the transaction. If no category and/or subcategory found relevant, leave it as NONE. If both are NONE for a transaction, don't include it in the output.",
        output_json=CategoryMappingList,
        expected_output='A verified JSON object containing the transactionId, and the corrected categoryId and subCategoryId (if applicable).',
        agent=agent,
    )
    return task.execute()

@app.route('/categorize', methods=['POST'])
def run_agents():
    print('Running agents...')
    data = request.get_json(force=True)
    
    crew = Crew(
        agents=[categorizer, verifier],
        tasks=[
            lambda: categorize_task(categorizer, data['transactions'], data['categories']),
            lambda: verify_task(verifier, data['transactions'], data['categories'])
        ],
        max_rpm=100,
        process=Process.sequential
    )
    
    result = crew.kickoff()
    return result, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
    agentops.end_session('Success')