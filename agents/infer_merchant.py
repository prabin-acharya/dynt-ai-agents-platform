from agents.base_agent import BaseAgent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_core.callbacks import UsageMetadataCallbackHandler
from prompts.infer_merchant import system_prompt_template, user_prompt_template
from agent_logs.supabase_logger_mixin import AgentLoggingMixin

llm = init_chat_model("openai:gpt-4o-mini")


class InferredMerchant(BaseModel):
    """Infer the merchant name from the transaction."""
    merchant_name: str = Field(description="The inferred merchant name.")
    transaction_id: str = Field(description="The ID of the transaction.")


# Wrap with structured output
structured_llm = llm.with_structured_output(InferredMerchant)



class InferMerchantAgent(BaseAgent, AgentLoggingMixin):
    def __init__(self):
        super().__init__("infer_merchant")

    def run(self, transaction):
        self._start_timer()
        callback = UsageMetadataCallbackHandler()


        # LLM call
        result = structured_llm.invoke([
            {
                "role": "system",
                "content": system_prompt_template
            },
            {
                "role": "user",
                "content": user_prompt_template.format(transaction=transaction)
            }
        ], config={"callbacks": [callback]})


        self._end_timer()
        
        self.log_agent_operation(
            agent_name=self.name,
            model_name="gpt-4o-mini",
            input_data={"transaction": transaction,},
            output_data=result.model_dump(),
            usage_metadata=callback.usage_metadata,
            key_name="transaction_id",
            key_id=transaction["id"]
        )

        return {
            "result": result.model_dump(),
            "usage_metadata": callback.usage_metadata
        }
    
