import logging
from typing import Dict, Any

class ErrorHandler:
    @staticmethod
    def handle_function_error(e: Exception, context: str) -> Dict[str, Any]:
        """
        Handle errors during function execution and return a standardized error response.

        Args:
            e (Exception): The exception that was raised.
            context (str): A string describing the context in which the error occurred.

        Returns:
            Dict[str, Any]: A dictionary containing the success status and error message.
        """
        logging.error(f"Error in {context}: {str(e)}")
        return {
            "success": False,
            "response": f"Error in {context}: {str(e)}",
            "error_type": type(e).__name__
        }