"""
MCP Tools module initialization - contains decorators and utilities for MCP tools.
"""
from functools import wraps
from typing import Callable, Any, Dict


def tool(name: str, description: str):
    """
    Decorator to register an MCP tool with metadata.
    
    Args:
        name: Name of the tool
        description: Description of what the tool does
    """
    def decorator(func: Callable) -> Callable:
        func._is_mcp_tool = True
        func._tool_name = name
        func._tool_description = description
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Note: validate_user_ownership is defined separately to avoid circular imports
# It's imported directly in the files that need it