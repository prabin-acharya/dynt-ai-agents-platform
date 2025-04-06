# categorize_transactions_agent.py
from agents.base_agent import BaseAgent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_core.callbacks import UsageMetadataCallbackHandler
from prompts.categorize_transaction import system_prompt_template, user_prompt_template
from agent_logs.supabase_logger_mixin import AgentLoggingMixin

llm = init_chat_model("openai:gpt-4o-mini")

# Custom schema
class Category(BaseModel):
    id: str = Field(description="Category ID")
    name: str = Field(description="Category name")

class TransactionCategory(BaseModel):
    """Classify the transaction to appropriate category."""
    reasoning: str = Field(description="Step-by-step reasoning behind the classification.")
    category: Category = Field(description="The category of the transaction.")
    transaction_id: str = Field(description="The ID of the transaction.")

# Wrap with structured output
structured_llm = llm.with_structured_output(TransactionCategory)

class CategorizeTransactionsAgent(BaseAgent, AgentLoggingMixin):
    def __init__(self):
        super().__init__("categorize_transaction")

    def run(self, transaction, categories):
        self._start_timer()
        callback = UsageMetadataCallbackHandler()

        system_prompt = system_prompt_template.format(
            categories=", ".join([f"{c['name']} (id: {c['id']})" for c in categories])
        )

        user_transaction_text = f"""Transaction ID: {transaction['id']}
        Amount: {transaction['amount']}
        Description: {transaction['description']}
        Merchant: {transaction['merchant']['name'] if transaction.get('merchant') else 'None'}
        """

        user_prompt = user_prompt_template.format(
            transaction=user_transaction_text
        )

        # LLM call
        result = structured_llm.invoke([
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ], config={"callbacks": [callback]})

        self._end_timer()
        
        self.log_agent_operation(
            agent_name=self.name,
            model_name="gpt-4o-mini",
            input_data={"transaction": transaction, "categories": categories},
            output_data=result.model_dump(),
            usage_metadata=callback.usage_metadata,
            key_name="transaction_id",
            key_id=transaction["id"]
        )

        return {
            "result": result.model_dump(),
            "usage_metadata": callback.usage_metadata
        }
    
