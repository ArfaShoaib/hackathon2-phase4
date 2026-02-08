"""
Main Todo AI Agent definition that processes natural language requests and uses MCP tools.
"""
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from routers.chat import ChatRequest
from mcp.tools.task_operations import add_task, list_tasks, complete_task, delete_task, update_task
from mcp.tools.error_handling import log_tool_call, log_tool_result, handle_tool_error
from models.conversation import Conversation, ConversationPublic
from models.message import Message, MessagePublic
from dependencies.database import get_session
from utils.logging import (
    log_chat_interaction, log_tool_usage, log_error,
    log_conversation_start, log_conversation_end
)
from sqlmodel import Session, select
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Add proper logging
logger = logging.getLogger(__name__)

# Configure Google Generative AI
GOOGLE_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GOOGLE_GEMINI_API_KEY:
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("DEBUG: Gemini API configured successfully")
else:
    logger.error("GEMINI_API_KEY not found in environment variables")
    print("DEBUG: GEMINI_API_KEY not found in environment variables")

async def process_chat_request(user_id: str, request: ChatRequest) -> Dict[str, Any]:
    """
    Process a chat request using AI logic and MCP tools.
    """
    print(f"DEBUG: Processing chat request for user_id: {user_id} (type: {type(user_id)})")
    
    # Convert user_id to integer for database operations
    # Handle both string and integer user IDs from Better Auth
    try:
        user_id_int = int(user_id)
        print(f"DEBUG: Successfully converted user_id to integer: {user_id_int}")
    except ValueError:
        print(f"DEBUG: User ID is not numeric: {user_id}, attempting to use as string")
        # If it's not numeric, it might be an email or UUID from Better Auth
        # In this case, we need to look up the numeric ID from the database
        # For now, let's try to handle it as a string ID that might map to a numeric ID
        user_id_int = await resolve_user_id(user_id)
        print(f"DEBUG: Resolved user_id to integer: {user_id_int}")

    try:
        # Load or create conversation
        conversation_id = await get_or_create_conversation(user_id_int, request.conversation_id)
        
        # Store user message
        await store_message(user_id_int, conversation_id, "user", request.message)
        
        # Get conversation history
        message_history = await get_message_history(conversation_id)
        
        # Process the user's request using GenAI
        response_data = await ai_process_request_with_genai(
            user_id_int,
            request.message,
            message_history
        )
        
        # Store AI response
        await store_message(user_id_int, conversation_id, "assistant", response_data["response"])
        
        return {
            "conversation_id": conversation_id,
            "response": response_data["response"],
            "tool_calls": response_data["tool_calls"]
        }
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Error in process_chat_request: {error_traceback}")
        raise


async def ai_process_request_with_genai(user_id: int, user_message: str, message_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Process the user's request using Google Generative AI.
    """
    # Check if the user is using name-based commands (contains quotes around task names)
    import re
    if re.search(r"'[^']*'|\"[^\"]*\"", user_message):
        # If user is using name-based commands (with quotes), use the rule-based processing
        # This ensures name-based operations work reliably
        print("DEBUG: Detected name-based command with quotes, using rule-based processing")
        return await ai_process_request(user_id, user_message, message_history)
    
    try:
        # Check if Gemini model is configured
        if not model:
            print("DEBUG: Gemini model not configured, using rule-based processing")
            return await ai_process_request(user_id, user_message, message_history)
        
        # Prepare the conversation context for the AI
        history_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_history[-5:]])  # Last 5 messages
        
        # Create a prompt that guides the AI to recognize task management commands
        prompt = f"""
        You are an AI assistant that helps manage tasks. The user can ask you to:
        - Add tasks: "Add task: Buy groceries" or "Create task: Call mom"
        - List tasks: "Show my tasks" or "List tasks"
        - Complete tasks: "Complete task #3", "Finish task #1", or "Complete task 'task name'"
        - Delete tasks: "Delete task #2", "Remove task #5", or "Delete task 'task name'"
        - Update tasks: "Update task #1: Buy organic groceries" or "Update task 'old name' to 'new name'"

        When the user refers to tasks by name instead of number, find the task by matching the name/title.
        For example:
        - "Complete task 'Buy groceries'" - find the task with title 'Buy groceries' and complete it
        - "Delete task 'Call mom'" - find the task with title 'Call mom' and delete it
        - "Update task 'Old task' to 'New task'" - find the task with title 'Old task' and update it

        Previous conversation:
        {history_context}

        User's current request:
        {user_message}

        Please respond with appropriate action.
        """
        
        print(f"DEBUG: Sending prompt to Gemini: {prompt[:100]}...")
        
        # Generate content using Gemini
        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                temperature=0.1,
                max_output_tokens=500
            )
        )
        
        print(f"DEBUG: Gemini response received: {response.text[:100]}...")
        
        # Process the response and execute appropriate actions
        # This is a simplified version - you might need more sophisticated parsing
        response_text = response.text
        return {
            "response": response_text,
            "tool_calls": []  # Will be populated based on intent detection
        }
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"DEBUG: Error in ai_process_request_with_genai: {error_traceback}")
        
        # Fallback to rule-based processing
        return await ai_process_request(user_id, user_message, message_history)


async def ai_process_request_fallback(user_id: int, user_message: str, message_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Fallback rule-based processing when GenAI fails.
    """
    print("DEBUG: Using fallback rule-based processing")
    
    # Identify the intent in the user message
    response_parts = []
    tool_calls = []

    # Process different types of requests
    user_lower = user_message.lower().strip()

    try:
        if "add task" in user_lower or "create task" in user_lower or "new task" in user_lower or user_lower.startswith("add "):
            # Extract task title (simple extraction)
            if user_lower.startswith("add task "):
                # Handle case where user says "add task" followed by the task
                task_text = user_lower[len("add task "):].strip()
            elif user_lower.startswith("create task "):
                # Handle case where user says "create task" followed by the task
                task_text = user_lower[len("create task "):].strip()
            elif user_lower.startswith("new task "):
                # Handle case where user says "new task" followed by the task
                task_text = user_lower[len("new task "):].strip()
            elif user_lower.startswith("add "):
                # Handle case where user just says "add" followed by the task
                task_text = user_lower[4:].strip()  # Remove "add " and get the rest
            else:
                # Handle existing cases - fallback
                task_text = user_lower.replace("add task", "").replace("create task", "").replace("new task", "").strip()
            
            if task_text.startswith("to ") or task_text.startswith("'") or task_text.startswith('"'):
                task_text = task_text[3:] if task_text.startswith("to ") else task_text
                task_text = task_text.strip().strip('\'"')

            if task_text:
                # Call add_task tool
                log_tool_call("add_task", {"user_id": user_id, "title": task_text})

                result = add_task(user_id=user_id, title=task_text)

                log_tool_result("add_task", result)
                log_tool_usage("add_task", str(user_id), {"user_id": user_id, "title": task_text}, result)

                response_parts.append(f"Task '{task_text}' has been created successfully.")
                tool_calls.append({
                    "tool_name": "add_task",
                    "parameters": {"user_id": user_id, "title": task_text},
                    "result": result
                })
            else:
                response_parts.append("I couldn't identify the task title. Please specify what task you'd like to add.")

        elif "show my tasks" in user_lower or "list tasks" in user_lower or "my tasks" in user_lower:
            # Call list_tasks tool
            log_tool_call("list_tasks", {"user_id": user_id})

            tasks = list_tasks(user_id=user_id, completed=None)

            log_tool_result("list_tasks", tasks)
            log_tool_usage("list_tasks", str(user_id), {"user_id": user_id}, tasks)

            if tasks:
                task_list_str = "\n".join([f"- [{task['id']}] {task['title']}" + (" (completed)" if task['completed'] else "") for task in tasks[:10]])  # Limit to 10 tasks
                response_parts.append(f"Here are your tasks:\n{task_list_str}")
            else:
                response_parts.append("You don't have any tasks yet.")

            tool_calls.append({
                "tool_name": "list_tasks",
                "parameters": {"user_id": user_id},
                "result": tasks
            })

        elif "complete task" in user_lower or "finish task" in user_lower or "done task" in user_lower:
            # Extract task ID
            import re
            task_id_match = re.search(r'#(\d+)', user_message) or re.search(r'task (\d+)', user_message)

            if task_id_match:
                task_id = int(task_id_match.group(1))

                # Call complete_task tool
                params = {"user_id": user_id, "task_id": task_id}
                log_tool_call("complete_task", params)

                result = complete_task(user_id=user_id, task_id=task_id)

                log_tool_result("complete_task", result)
                log_tool_usage("complete_task", str(user_id), params, result)

                response_parts.append(f"Task #{task_id} has been marked as completed.")
                tool_calls.append({
                    "tool_name": "complete_task",
                    "parameters": {"user_id": user_id, "task_id": task_id},
                    "result": result
                })
            else:
                response_parts.append("I couldn't identify which task to complete. Please specify the task number (e.g., 'complete task #5').")

        elif "delete task" in user_lower or "remove task" in user_lower:
            # Extract task ID
            import re
            task_id_match = re.search(r'#(\d+)', user_message) or re.search(r'task (\d+)', user_message)

            if task_id_match:
                task_id = int(task_id_match.group(1))

                # Call delete_task tool
                params = {"user_id": user_id, "task_id": task_id}
                log_tool_call("delete_task", params)

                result = delete_task(user_id=user_id, task_id=task_id)

                log_tool_result("delete_task", result)
                log_tool_usage("delete_task", str(user_id), params, result)

                response_parts.append(f"Task #{task_id} has been deleted.")
                tool_calls.append({
                    "tool_name": "delete_task",
                    "parameters": {"user_id": user_id, "task_id": task_id},
                    "result": result
                })
            else:
                response_parts.append("I couldn't identify which task to delete. Please specify the task number (e.g., 'delete task #5').")

        elif "update task" in user_lower or "change task" in user_lower or "edit task" in user_lower:
            # Extract task ID and new title
            import re
            # Look for patterns like "update task #1 to 'new title'"
            pattern = r"(?:update task|change task|edit task)\s+#?(\d+)\s+(?:to|as)\s+(?:'|\"|)(.*?)(?:'|\"|)$"
            match = re.search(pattern, user_message, re.IGNORECASE)

            if match:
                task_id = int(match.group(1))
                new_title = match.group(2).strip()

                # Call update_task tool
                params = {
                    "user_id": user_id,
                    "task_id": task_id,
                    "title": new_title
                }
                log_tool_call("update_task", params)

                result = update_task(
                    user_id=user_id,
                    task_id=task_id,
                    title=new_title
                )

                log_tool_result("update_task", result)
                log_tool_usage("update_task", str(user_id), params, result)

                response_parts.append(f"Task #{task_id} has been updated to '{new_title}'.")
                tool_calls.append({
                    "tool_name": "update_task",
                    "parameters": {
                        "user_id": user_id,
                        "task_id": task_id,
                        "title": new_title
                    },
                    "result": result
                })
            else:
                response_parts.append("I couldn't identify the task to update and its new details. Please use a format like 'update task #1 to \"new title\"'.")

        else:
            # Default response for unrecognized commands
            response_parts.append("I can help you manage your tasks. You can ask me to: add tasks, list tasks, complete tasks, delete tasks, or update tasks. For example: 'Add a task to buy groceries' or 'Show my pending tasks'.")

    except Exception as e:
        # Handle any errors during tool execution
        import traceback
        error_traceback = traceback.format_exc()
        log_error(f"Error in ai_process_request_fallback: {str(e)}\nTraceback: {error_traceback}", user_id=str(user_id))
        error_response = handle_tool_error("ai_process_request_fallback", e)
        response_parts.append(f"Sorry, I encountered an error processing your request: {error_response['error']}")

    # Join all response parts
    final_response = " ".join(response_parts) if response_parts else "I'm not sure how to help with that. You can ask me to add, list, complete, delete, or update tasks."

    return {
        "response": final_response,
        "tool_calls": tool_calls
    }


async def get_or_create_conversation(user_id: int, conversation_id: str = None) -> str:
    """
    Get existing conversation or create a new one.

    Args:
        user_id: The ID of the user
        conversation_id: Optional existing conversation ID

    Returns:
        The conversation ID
    """
    from dependencies.database import get_session_context

    with get_session_context() as session:
        if conversation_id is not None:
            try:
                # Convert conversation_id to int to match database type
                conv_id = int(conversation_id)
                # Check if conversation exists and belongs to user
                statement = select(Conversation).where(
                    Conversation.id == conv_id,
                    Conversation.user_id == user_id
                )
                conversation = session.exec(statement).first()

                if conversation:
                    # Update the conversation's updated_at timestamp
                    conversation.updated_at = datetime.now()
                    session.add(conversation)
                    session.commit()

                    return str(conversation.id)  # Return as string
            except (ValueError, TypeError):
                # If conversation_id is invalid, proceed to create a new one
                pass

        # Create a new conversation
        new_conversation = Conversation(user_id=user_id)
        session.add(new_conversation)
        session.commit()
        session.refresh(new_conversation)

        # Log conversation start
        log_conversation_start(user_id, str(new_conversation.id))

        return str(new_conversation.id)  # Return as string


async def store_message(user_id: int, conversation_id: str, role: str, content: str) -> MessagePublic:
    """
    Store a message in the conversation.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation
        role: The role of the message sender ("user" or "assistant")
        content: The content of the message

    Returns:
        The created message
    """
    from dependencies.database import get_session_context
    with get_session_context() as session:
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        # Log the message storage
        if role == "user":
            log_chat_interaction(user_id, conversation_id, content, "")
        elif role == "assistant":
            log_chat_interaction(user_id, conversation_id, "", content)

        # Return a public representation of the message
        return MessagePublic(
            user_id=message.user_id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            id=message.id,
            created_at=message.created_at
        )


async def get_message_history(conversation_id: str) -> List[Dict[str, str]]:
    """
    Get the message history for a conversation.

    Args:
        conversation_id: The ID of the conversation

    Returns:
        List of messages with role and content
    """
    from dependencies.database import get_session_context

    with get_session_context() as session:
        # Convert conversation_id to int for database query
        try:
            conv_id = int(conversation_id) if conversation_id else None
        except (ValueError, TypeError):
            # If conversation_id is not a valid integer, return empty list
            return []
        
        if conv_id is not None:
            statement = select(Message).where(
                Message.conversation_id == conv_id
            ).order_by(Message.created_at.asc())
        else:
            # If no conversation_id provided, return empty list
            return []

        messages = session.exec(statement).all()

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]


async def ai_process_request(user_id: int, user_message: str, message_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Process the user's request using AI logic and appropriate tools.

    Args:
        user_id: The ID of the authenticated user
        user_message: The user's message
        message_history: The conversation history

    Returns:
        Dictionary with response and tool calls
    """
    # This is a simplified version of AI processing
    # In a real implementation, this would connect to Gemini via a compatibility layer

    # Identify the intent in the user message
    response_parts = []
    tool_calls = []

    # Process different types of requests
    user_lower = user_message.lower().strip()

    try:
        if "add task" in user_lower or "create task" in user_lower or "new task" in user_lower or user_lower.startswith("add "):
            # Extract task title (simple extraction)
            if user_lower.startswith("add task "):
                # Handle case where user says "add task" followed by the task
                task_text = user_lower[len("add task "):].strip()
            elif user_lower.startswith("create task "):
                # Handle case where user says "create task" followed by the task
                task_text = user_lower[len("create task "):].strip()
            elif user_lower.startswith("new task "):
                # Handle case where user says "new task" followed by the task
                task_text = user_lower[len("new task "):].strip()
            elif user_lower.startswith("add "):
                # Handle case where user just says "add" followed by the task
                task_text = user_lower[4:].strip()  # Remove "add " and get the rest
            else:
                # Handle existing cases - fallback
                task_text = user_lower.replace("add task", "").replace("create task", "").replace("new task", "").strip()
            
            if task_text.startswith("to ") or task_text.startswith("'") or task_text.startswith('"'):
                task_text = task_text[3:] if task_text.startswith("to ") else task_text
                task_text = task_text.strip().strip('\'"')

            if task_text:
                # Call add_task tool
                log_tool_call("add_task", {"user_id": user_id, "title": task_text})

                result = add_task(user_id=user_id, title=task_text)

                log_tool_result("add_task", result)
                log_tool_usage("add_task", str(user_id), {"user_id": user_id, "title": task_text}, result)

                response_parts.append(f"Task '{task_text}' has been created successfully.")
                tool_calls.append({
                    "tool_name": "add_task",
                    "parameters": {"user_id": user_id, "title": task_text},
                    "result": result
                })
            else:
                response_parts.append("I couldn't identify the task title. Please specify what task you'd like to add.")

        elif "show my tasks" in user_lower or "list tasks" in user_lower or "my tasks" in user_lower:
            # Check if user wants completed, pending, or all tasks
            completed_filter = None
            if "completed" in user_lower:
                completed_filter = True
            elif "pending" in user_lower or "incomplete" in user_lower:
                completed_filter = False

            # Call list_tasks tool
            params = {"user_id": user_id, "completed": completed_filter}
            log_tool_call("list_tasks", params)

            tasks = list_tasks(user_id=user_id, completed=completed_filter)

            log_tool_result("list_tasks", tasks)
            log_tool_usage("list_tasks", str(user_id), params, tasks)

            if tasks:
                task_list_str = "\n".join([f"- {task['title']}" for task in tasks[:10]])  # Limit to 10 tasks
                if completed_filter is True:
                    response_parts.append(f"Here are your completed tasks:\n{task_list_str}")
                elif completed_filter is False:
                    response_parts.append(f"Here are your pending tasks:\n{task_list_str}")
                else:
                    response_parts.append(f"Here are your tasks:\n{task_list_str}")
            else:
                if completed_filter is True:
                    response_parts.append("You don't have any completed tasks.")
                elif completed_filter is False:
                    response_parts.append("You don't have any pending tasks.")
                else:
                    response_parts.append("You don't have any tasks yet.")

            tool_calls.append({
                "tool_name": "list_tasks",
                "parameters": {"user_id": user_id, "completed": completed_filter},
                "result": tasks
            })

        elif "complete task" in user_lower or "finish task" in user_lower or "done task" in user_lower:
            # First, try to find by title (prioritized)
            task_title = ""
            import re
            
            # Pattern to match task title in quotes
            quote_pattern = r'(?:complete task|finish task|done task)\s+(?:\'|"|)(.*?)(?:\'|"|)\s*$'
            quote_match = re.search(quote_pattern, user_message, re.IGNORECASE)
            
            if quote_match:
                task_title = quote_match.group(1).strip()
            else:
                # Pattern to match task title without quotes
                no_quote_pattern = r'(?:complete task|finish task|done task)\s+(.+)$'
                no_quote_match = re.search(no_quote_pattern, user_message, re.IGNORECASE)
                
                if no_quote_match:  # Fixed: was checking the pattern instead of the match
                    task_title = no_quote_match.group(1).strip().strip('\'"')
            
            # If we found a title, try to match it
            if task_title:
                # Get all tasks to find the one with the exact matching title
                all_tasks = list_tasks(user_id=user_id, completed=False)

                matched_task = None
                for task in all_tasks:
                    if task_title.lower() == task['title'].lower():  # Exact match first
                        matched_task = task
                        break
                
                # If no exact match, try partial match
                if not matched_task:
                    for task in all_tasks:
                        if task_title.lower() in task['title'].lower():
                            matched_task = task
                            break

                if matched_task:
                    # Call complete_task tool
                    params = {"user_id": user_id, "task_id": matched_task['id']}
                    log_tool_call("complete_task", params)

                    result = complete_task(user_id=user_id, task_id=matched_task['id'])

                    log_tool_result("complete_task", result)
                    log_tool_usage("complete_task", str(user_id), params, result)

                    response_parts.append(f"Task '{matched_task['title']}' has been marked as completed.")
                    tool_calls.append({
                        "tool_name": "complete_task",
                        "parameters": {"user_id": user_id, "task_id": matched_task['id']},
                        "result": result
                    })
                else:
                    response_parts.append(f"I couldn't find a task named '{task_title}'. Please check the task name.")
            else:
                # If no title found, then try to extract ID as fallback
                task_id_match = re.search(r'#(\d+)', user_message) or re.search(r'task (\d+)', user_message)

                if task_id_match:
                    task_id = int(task_id_match.group(1))

                    # Call complete_task tool
                    params = {"user_id": user_id, "task_id": task_id}
                    log_tool_call("complete_task", params)

                    result = complete_task(user_id=user_id, task_id=task_id)

                    log_tool_result("complete_task", result)
                    log_tool_usage("complete_task", str(user_id), params, result)

                    response_parts.append(f"Task #{task_id} has been marked as completed.")
                    tool_calls.append({
                        "tool_name": "complete_task",
                        "parameters": {"user_id": user_id, "task_id": task_id},
                        "result": result
                    })
                else:
                    response_parts.append(f"I couldn't find a task named '{task_title}'. Please specify the task name to complete.")

        elif "delete task" in user_lower or "remove task" in user_lower:
            # First, try to find by title (prioritized)
            task_title = ""
            # Extract task title from various formats like "delete task 'title'", "delete task title", etc.
            import re
            
            # Pattern to match task title in quotes
            quote_pattern = r'(?:delete task|remove task)\s+(?:\'|"|)(.*?)(?:\'|"|)\s*$'
            quote_match = re.search(quote_pattern, user_message, re.IGNORECASE)
            
            if quote_match:
                task_title = quote_match.group(1).strip()
            else:
                # Pattern to match task title without quotes
                no_quote_pattern = r'(?:delete task|remove task)\s+(.+)$'
                no_quote_match = re.search(no_quote_pattern, user_message, re.IGNORECASE)
                
                if no_quote_match:
                    task_title = no_quote_match.group(1).strip().strip('\'"')
            
            # If we found a title, try to match it
            if task_title:
                # Get all tasks to find the one with the exact matching title
                all_tasks = list_tasks(user_id=user_id, completed=None)

                matched_task = None
                for task in all_tasks:
                    if task_title.lower() == task['title'].lower():  # Exact match first
                        matched_task = task
                        break
                
                # If no exact match, try partial match
                if not matched_task:
                    for task in all_tasks:
                        if task_title.lower() in task['title'].lower():
                            matched_task = task
                            break

                if matched_task:
                    # Call delete_task tool
                    params = {"user_id": user_id, "task_id": matched_task['id']}
                    log_tool_call("delete_task", params)

                    result = delete_task(user_id=user_id, task_id=matched_task['id'])

                    log_tool_result("delete_task", result)
                    log_tool_usage("delete_task", str(user_id), params, result)

                    response_parts.append(f"Task '{matched_task['title']}' has been deleted.")
                    tool_calls.append({
                        "tool_name": "delete_task",
                        "parameters": {"user_id": user_id, "task_id": matched_task['id']},
                        "result": result
                    })
                else:
                    response_parts.append(f"I couldn't find a task named '{task_title}'. Please check the task name.")
            else:
                # If no title found, then try to extract ID as fallback
                task_id_match = re.search(r'#(\d+)', user_message) or re.search(r'task (\d+)', user_message)

                if task_id_match:
                    task_id = int(task_id_match.group(1))

                    # Call delete_task tool
                    params = {"user_id": user_id, "task_id": task_id}
                    log_tool_call("delete_task", params)

                    result = delete_task(user_id=user_id, task_id=task_id)

                    log_tool_result("delete_task", result)
                    log_tool_usage("delete_task", str(user_id), params, result)

                    response_parts.append(f"Task #{task_id} has been deleted.")
                    tool_calls.append({
                        "tool_name": "delete_task",
                        "parameters": {"user_id": user_id, "task_id": task_id},
                        "result": result
                    })
                else:
                    response_parts.append(f"I couldn't find a task named '{task_title}'. Please specify the task name to delete.")

        elif "update task" in user_lower or "change task" in user_lower or "edit task" in user_lower:
            # Extract old title and new title
            import re
            # Look for patterns like "change task 'old title' to 'new title'"
            pattern = r"(?:change task|update task|edit task)\s+(?:'|\"|)(.*?)(?:'|\"|)\s+to\s+(?:'|\"|)(.*?)(?:'|\"|)$"
            match = re.search(pattern, user_message, re.IGNORECASE)

            if match:
                old_title = match.group(1).strip()
                new_title = match.group(2).strip()

                # Find the task with the old title
                all_tasks = list_tasks(user_id=user_id, completed=None)

                matched_task = None
                for task in all_tasks:
                    if old_title.lower() in task['title'].lower():
                        matched_task = task
                        break

                if matched_task:
                    # Call update_task tool
                    params = {
                        "user_id": user_id,
                        "task_id": matched_task['id'],
                        "title": new_title
                    }
                    log_tool_call("update_task", params)

                    result = update_task(
                        user_id=user_id,
                        task_id=matched_task['id'],
                        title=new_title
                    )

                    log_tool_result("update_task", result)
                    log_tool_usage("update_task", str(user_id), params, result)

                    response_parts.append(f"Task '{old_title}' has been updated to '{new_title}'.")
                    tool_calls.append({
                        "tool_name": "update_task",
                        "parameters": {
                            "user_id": user_id,
                            "task_id": matched_task['id'],
                            "title": new_title
                        },
                        "result": result
                    })
                else:
                    response_parts.append(f"I couldn't find a task matching '{old_title}'. Please check the task name.")
            else:
                response_parts.append("I couldn't identify the task to update and its new details. Please use a format like 'change task \"old title\" to \"new title\"'.")

        else:
            # Default response for unrecognized commands
            response_parts.append("I can help you manage your tasks. You can ask me to: add tasks, list tasks, complete tasks, delete tasks, or update tasks. For example: 'Add a task to buy groceries' or 'Show my pending tasks'.")

    except Exception as e:
        # Handle any errors during tool execution
        import traceback
        error_traceback = traceback.format_exc()
        log_error(f"Error in ai_process_request: {str(e)}\nTraceback: {error_traceback}", user_id=str(user_id))
        error_response = handle_tool_error("ai_process_request", e)
        response_parts.append(f"Sorry, I encountered an error processing your request: {error_response['error']}")

    # Join all response parts
    final_response = " ".join(response_parts) if response_parts else "I'm not sure how to help with that. You can ask me to add, list, complete, delete, or update tasks."

    return {
        "response": final_response,
        "tool_calls": tool_calls
    }


async def resolve_user_id(jwt_user_id: str) -> int:
    """
    Resolve JWT user ID to database user ID.

    Args:
        jwt_user_id: The user ID from JWT token (could be string representation)

    Returns:
        The corresponding integer database user ID
    """
    # This is a placeholder implementation
    # In a real system, this would map JWT identifiers to database user IDs
    # This could involve looking up by email, external ID, etc.

    # For this implementation, let's assume the jwt_user_id corresponds
    # to an email or some other unique identifier in the User table
    from dependencies.database import get_session_context
    from models.user import User
    from sqlmodel import select

    with get_session_context() as session:
        # If jwt_user_id looks like an email, try to find by email
        if '@' in jwt_user_id:
            statement = select(User).where(User.email == jwt_user_id)
        else:
            # If it's not an email, assume it's the string representation of the integer ID
            # This is a common scenario where JWT contains the user ID as string
            try:
                return int(jwt_user_id)
            except ValueError:
                # If not a numeric string, we might have a more complex ID format
                # In a real implementation, this would involve more sophisticated lookup
                raise ValueError(f"Cannot resolve user ID: {jwt_user_id}")

        user = session.exec(statement).first()

        if not user:
            raise ValueError(f"User not found: {jwt_user_id}")

        return user.id