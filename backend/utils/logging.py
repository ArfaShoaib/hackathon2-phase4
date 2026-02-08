"""
Comprehensive logging throughout the chat system.
"""
import logging
from datetime import datetime
from typing import Any, Dict


# Set up the main logger for the chat system
chat_logger = logging.getLogger("chatbot")
chat_logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handler to logger
chat_logger.addHandler(console_handler)
chat_logger.propagate = False  # Prevent double logging


def log_chat_interaction(user_id: str, conversation_id: str, user_message: str, ai_response: str) -> None:
    """
    Log a complete chat interaction between user and AI.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation
        user_message: The message sent by the user
        ai_response: The response from the AI
    """
    chat_logger.info(
        f"Chat Interaction | User: {user_id} | "
        f"Conversation: {conversation_id} | "
        f"User: {user_message[:50]}{'...' if len(user_message) > 50 else ''} | "
        f"AI: {ai_response[:50]}{'...' if len(ai_response) > 50 else ''}"
    )


def log_tool_usage(tool_name: str, user_id: str, params: Dict[str, Any], result: Any) -> None:
    """
    Log when an MCP tool is used.

    Args:
        tool_name: Name of the tool being used
        user_id: The ID of the user who triggered the tool
        params: Parameters passed to the tool
        result: Result returned by the tool
    """
    chat_logger.info(
        f"MCP Tool Usage | Tool: {tool_name} | User: {user_id} | "
        f"Params: {str(params)[:100]}{'...' if len(str(params)) > 100 else ''} | "
        f"Result: {'Success' if result else 'Failed'}"
    )


def log_error(error_msg: str, user_id: str = None, conversation_id: str = None) -> None:
    """
    Log an error in the chat system.

    Args:
        error_msg: The error message
        user_id: Optional user ID involved in the error
        conversation_id: Optional conversation ID involved in the error
    """
    context = ""
    if user_id:
        context += f" | User: {user_id}"
    if conversation_id:
        context += f" | Conversation: {conversation_id}"

    chat_logger.error(f"Chat System Error{context} | {error_msg}")


def log_authentication_event(event_type: str, user_id: str = None, details: str = None) -> None:
    """
    Log authentication-related events.

    Args:
        event_type: Type of authentication event (login, logout, validation, etc.)
        user_id: The ID of the user involved
        details: Additional details about the event
    """
    chat_logger.info(f"Auth Event | Type: {event_type} | User: {user_id or 'Unknown'} | Details: {details or 'N/A'}")


def log_conversation_start(user_id: str, conversation_id: str) -> None:
    """
    Log when a conversation starts.

    Args:
        user_id: The ID of the user starting the conversation
        conversation_id: The ID of the new conversation
    """
    chat_logger.info(f"Conversation Started | User: {user_id} | ID: {conversation_id}")


def log_conversation_end(user_id: str, conversation_id: str, duration_seconds: float) -> None:
    """
    Log when a conversation ends.

    Args:
        user_id: The ID of the user ending the conversation
        conversation_id: The ID of the ended conversation
        duration_seconds: Duration of the conversation in seconds
    """
    chat_logger.info(
        f"Conversation Ended | User: {user_id} | ID: {conversation_id} | "
        f"Duration: {duration_seconds:.2f}s"
    )


def log_api_call(endpoint: str, user_id: str, request_size: int, response_size: int, duration_ms: float) -> None:
    """
    Log API call details.

    Args:
        endpoint: The API endpoint called
        user_id: The ID of the user making the call
        request_size: Size of the request in bytes
        response_size: Size of the response in bytes
        duration_ms: Duration of the call in milliseconds
    """
    chat_logger.info(
        f"API Call | Endpoint: {endpoint} | User: {user_id} | "
        f"ReqSize: {request_size}B | ResSize: {response_size}B | "
        f"Duration: {duration_ms:.2f}ms"
    )