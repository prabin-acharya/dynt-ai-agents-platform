from agents.base_agent import BaseAgent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_core.callbacks import UsageMetadataCallbackHandler
from prompts.infer_merchant import system_prompt_template, user_prompt_template
from agent_logs.supabase_logger_mixin import AgentLoggingMixin
from config import Config
import logging

logger = logging.getLogger(__name__)


llm = init_chat_model(Config.LLM_MODEL_NAME)


class InferredMerchant(BaseModel):
    """Infer the merchant name from the transaction."""
    merchant_name: str = Field(description="The inferred merchant name.")
    transaction_id: str = Field(description="The ID of the transaction.")


# Wrap with structured output
structured_llm = llm.with_structured_output(InferredMerchant)


class InferMerchantAgent(BaseAgent, AgentLoggingMixin):
    def __init__(self):
        super().__init__("infer_merchants")

    def run(self, transaction):
        self._start_timer()
        callback = UsageMetadataCallbackHandler()

        try:
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


            output_data = result.model_dump()
            output_data["transaction_id"] = transaction.get("id")  # ensure original ID
            status = "success"

        except Exception as e:
            logger.exception(f"Failed to infer merchant for transaction ID: {transaction.get('id')}")
            output_data = {
                "error": str(e),
                "transaction_id": transaction.get("id"),
            }
            status = "error"

        finally:
            self._end_timer()

            self.log_agent_operation(
                agent_name=self.name,
                model_name=Config.LLM_MODEL_NAME,
                input_data={"transaction": transaction},
                output_data=output_data,
                usage_metadata=callback.usage_metadata if status == "success" else None,
                key_name="transaction_id",
                key_id=transaction.get("id")
            )

        return {
            "result": output_data,
            "usage_metadata": callback.usage_metadata if status == "success" else None,
            "status": status
        }