"""
Common error handling and logging for MCP tools.
"""
import logging
from typing import Any, Dict
from utils.errors import ChatBotError


# Set up logging for MCP tools
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler for tool-specific logging
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_tool_call(tool_name: str, params: Dict[str, Any]) -> None:
    """
    Log a tool call with its parameters.

    Args:
        tool_name: Name of the tool being called
        params: Parameters passed to the tool
    """
    logger.info(f"MCP Tool Called: {tool_name} with params: {params}")


def log_tool_result(tool_name: str, result: Any) -> None:
    """
    Log the result of a tool call.

    Args:
        tool_name: Name of the tool that was called
        result: Result returned by the tool
    """
    logger.info(f"MCP Tool Result: {tool_name} returned: {result}")


def log_tool_error(tool_name: str, error: Exception) -> None:
    """
    Log an error from a tool call.

    Args:
        tool_name: Name of the tool that encountered an error
        error: Exception that occurred
    """
    logger.error(f"MCP Tool Error: {tool_name} encountered error: {str(error)}")


def handle_tool_error(tool_name: str, error: Exception) -> Dict[str, Any]:
    """
    Handle an error from a tool call and return a standardized error response.

    Args:
        tool_name: Name of the tool that encountered an error
        error: Exception that occurred

    Returns:
        Dictionary with error details
    """
    log_tool_error(tool_name, error)

    if isinstance(error, ChatBotError):
        return {
            "error": error.message,
            "error_code": error.error_code,
            "status_code": error.status_code
        }
    else:
        # For unexpected errors, return a generic response
        return {
            "error": f"An error occurred in {tool_name}: {str(error)}",
            "error_code": "UNEXPECTED_ERROR",
            "status_code": 500
        }