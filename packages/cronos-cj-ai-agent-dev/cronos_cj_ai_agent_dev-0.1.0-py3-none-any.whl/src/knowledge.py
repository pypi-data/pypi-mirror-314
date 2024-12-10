import os
import cohere
from src.logger import logger

class Knowledge:
    def __init__(self):
        self.cohere_api_key = os.environ.get("COHERE_API_KEY", "")
        self.cohere_client = cohere.Client(api_key=self.cohere_api_key)

    def query_cronos_zkevm_knowledge_base(
        self,
        message: str,
        chat_history: list[dict],
    ):
        """
        This uses V1
        chat_history can be from User, Assistant, Tool and System roles.
        chat_history should be in the following format:
        [
            {"role": "User", "message": "What are the yield bearing tokens on Cronos zkEVM ?"},
            {"role": "Assistant", "message": (
                "The Cronos zkEVM blockchain supports yield-bearing "
                "tokens as first-class citizens..."},
        ]
        """
        try:
            response = self.cohere_client.chat(
                model="command-r-plus-08-2024",
                message=message,
                chat_history=chat_history,
                prompt_truncation="AUTO",
                temperature=0.3,
                connectors=[
                    {
                        "id": "web-search",
                        "options": {"site": "https://docs-zkevm.cronos.org/"},
                    }
                ],
            )
            response_text = response.text
            response_sources = []
            for source in response.documents:
                response_sources.append(source.get("url", ""))
            if len(response_sources) > 0:
                response_text = response_text + "\n\nSources:\n" + "\n".join(response_sources)
            return response_text
        except Exception as e:
            logger.error("Error:", e)
            return "I was not able to find the answer to your question."
