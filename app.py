
import os
from dotenv import load_dotenv
import agentops
from flask import Flask, request, jsonify
from crewai import Agent, Task, Crew, Process
from typing import List, Optional
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize AgentOps with your API key from .env
agentops.init(os.getenv('AGENTOPS_API_KEY'))

# Set up OpenAI environment variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

class CategoryMapping(BaseModel):
    transactionId: str
    categoryId: Optional[str] = None
    subCategoryId: Optional[str] = None

class CategoryMappingList(BaseModel):
    mappings: List[CategoryMapping]

app = Flask(__name__)

categorizer = Agent(
    role='Senior Transaction Categorizer',
    goal='Categorize transactions with predefined categories and subcategories',
    backstory="You work at a big accounting company and trained to understand and categorize financial transactions. You analyze transaction details like description, merchant name, debit/credit and categorize them into predefined categories and subcategories",
    allow_delegation=False,
)

verifier = Agent(
    role='Senior Transaction Verifier',
    goal='Verify the categories and subcategories of transactions',
    backstory="You work at a big accounting firm and trained to verify the categories and subcategories of financial transactions. You cross-check the categorized transactions and ensure their accuracy.",
    allow_delegation=True,
)

def categorize_task(agent, transactions, categories, instructions):
    task = Task(
        description=f"Categorize the given transactions: {transactions} based on their details into one of the predefined list of categories and subcategories: {categories}, remember a subcategory can only be assigned if the parent category is assigned to that transaction. Make sure you thoroughly follow the instructions: {instructions} while categorizing the transactions.",
        expected_output='JSON object containing the transaction details and its category and subcategory (if applicable).',
        agent=agent,
    )
    return task

def verify_task(agent, transactions, categories, instructions):
    task = Task(
        description=f"Verify the category of the given transactions: {transactions} based on their details. If the category and/or subcategory is incorrect, correct it. The possible categories are {categories}. Remember a subcategory can only be assigned if the parent category is assigned added to the transaction. If no category and/or subcategory found relevant, leave it. If both couldn't be found for a transaction, don't include it in the output. Make sure you thoroughly follow the instructions (if any): {instructions} while verifying the transactions.",
        output_json=CategoryMappingList,
        expected_output='A verified JSON object containing the transactionId, and the corrected categoryId and subCategoryId (if applicable).',
        agent=agent,
    )
    return task

@app.route('/categorize', methods=['POST'])
def run_agents():
    print('Running agents...')
    data = request.get_json(force=True)

    crew = Crew(
        agents=[categorizer, verifier],
        tasks=[
            categorize_task(categorizer, data['transactions'], data['categories'], data['instructions']),
            verify_task(verifier, data['transactions'], data['categories'], data['instructions'])
        ],
        max_rpm=100,
        process=Process.sequential
    )

    result = crew.kickoff()
    return result.model_dump_json(), 200







class InferMerchant(BaseModel):
    transactionId: str
    merchant: Optional[str] = None

class InferMerchantList(BaseModel):
    transactions: List[InferMerchant]

merchant_inferer = Agent(
    role='Advanced Merchant Detection Specialist',
    goal='Accurately determine the merchant name from detailed transaction descriptions',
    backstory="As an AI developed by a leading fintech company, you've been trained on millions of transaction records to identify merchant names with high precision, even from the most ambiguous transaction descriptions.",
    allow_delegation=False,
)

def infer_merchant_task(agent, transactions, instructions):
    task = Task(
        description=f"Analyze the provided list of transaction details: {transactions} and apply your advanced inference algorithms to accurately identify the merchant names. Each transaction is a puzzle, and your role is to solve it with the precision of a detective. Make sure you follow the given instructions: {instructions} while inferring the merchant names.",
        expected_output="A structured list of JSON objects, each containing 'transactionId', and the inferred 'merchantName' (if found) for that transaction. Accuracy is key, as these inferences power critical financial analytics.",
        agent=agent,
        output_json=InferMerchantList,
    )
    return task


@app.route('/infer_merchant', methods=['POST'])
def run_merchant_inference():
    data = request.get_json(force=True)
    print('Running merchant agent...')

    crew = Crew(
        agents=[merchant_inferer],
        tasks=[infer_merchant_task(merchant_inferer, data["transactions"], data["instructions"])],
        max_rpm=100,
        process=Process.sequential
    )

    result = crew.kickoff()
    return result.model_dump_json(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)

