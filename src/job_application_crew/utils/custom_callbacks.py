# job_application_crew/utils/custom_callbacks.py
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class TokenCountingCallback(BaseCallbackHandler):
    """Callback handler for counting tokens."""

    def __init__(self):
        self.total_tokens_used = 0
        self.prompt_tokens_used = 0
        self.completion_tokens_used = 0

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Run when LLM ends running."""
        if response.llm_output:
            token_usage = response.llm_output.get("token_usage")
            if token_usage:
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                total_tokens_for_call = token_usage.get("total_tokens", 0)

                self.prompt_tokens_used += prompt_tokens
                self.completion_tokens_used += completion_tokens
                self.total_tokens_used += total_tokens_for_call

                print(f"\n--- LLM Call Ended ---")
                print(f"  Prompt Tokens: {prompt_tokens}")
                print(f"  Completion Tokens: {completion_tokens}")
                print(f"  Total Tokens for this call: {total_tokens_for_call}")
                print(f"  Cumulative Total Tokens: {self.total_tokens_used}")
                print(f"----------------------\n")

    def __str__(self):
        return (f"\n--- Overall Token Usage Summary --- \n"
                f"Total Tokens Across All Calls: {self.total_tokens_used}\n"
                f"Total Prompt Tokens: {self.prompt_tokens_used}\n"
                f"Total Completion Tokens: {self.completion_tokens_used}\n"
                f"-----------------------------------\n")