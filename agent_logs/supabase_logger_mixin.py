from datetime import datetime, timezone
import time
import json
from agent_logs.supabase_client import supabase


class AgentLoggingMixin:
    def _start_timer(self):
        self._start_time = time.time()

    def _end_timer(self):
        self._duration = time.time() - self._start_time

    def log_agent_operation(self, *, agent_name, model_name, input_data, output_data, usage_metadata, key_name=None, key_id=None):
        log_data = {
            "agent_name": agent_name,
            "key_name": key_name,
            "key_id": key_id,
            "input": input_data,
            "output": output_data,
            "duration_secs": self._duration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_name": model_name,
            "tokens_used": usage_metadata,
        }

        print("\n=== Agent Log ===")
        print(json.dumps(log_data, indent=2))
        print("=================\n")

        try:
            supabase.table("AgentLogs").insert(log_data).execute()
        except Exception as e:
            print(f"Logging to Supabase failed: {e}")
