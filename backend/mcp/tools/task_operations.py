"""
MCP tools for task operations that allow the AI agent to manage user tasks.
Each tool is decorated with the @tool decorator to make it available to the AI agent.
"""
from typing import List, Optional
from datetime import datetime
from models.task import Task
from dependencies.database import get_session_context
from utils.errors import ValidationError, AuthorizationError
from . import tool
from sqlmodel import Session, select


@tool(
    name="add_task",
    description="Add a new task for a user with the specified details"
)
def add_task(user_id: int, title: str, description: Optional[str] = None) -> dict:
    """
    Add a new task for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task creation details
    """
    # Validate input
    if not title or len(title.strip()) == 0:
        raise ValidationError("Task title is required")

    with get_session_context() as session:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }


@tool(
    name="list_tasks",
    description="List tasks for a user with optional filtering by completion status"
)
def list_tasks(user_id: int, completed: Optional[bool] = None) -> List[dict]:
    """
    List tasks for the specified user with optional filtering by completion status.

    Args:
        user_id: The ID of the user whose tasks to list
        completed: Optional filter for completion status (None=all, True=completed, False=pending)

    Returns:
        List of task dictionaries
    """
    with get_session_context() as session:
        # Build query based on filters
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        query = query.order_by(Task.created_at.desc())
        tasks = session.exec(query).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]


@tool(
    name="complete_task",
    description="Mark a specific task as completed for a user"
)
def complete_task(user_id: int, task_id: int) -> dict:
    """
    Mark a specific task as completed for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as completed

    Returns:
        Dictionary with task completion details
    """
    with get_session_context() as session:
        # Find the task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise ValidationError(f"Task with ID {task_id} not found for user {user_id}")

        # Update task as completed
        task.completed = True
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title,
            "completed": task.completed
        }


@tool(
    name="delete_task",
    description="Delete a specific task for a user"
)
def delete_task(user_id: int, task_id: int) -> dict:
    """
    Delete a specific task for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete

    Returns:
        Dictionary with task deletion details
    """
    with get_session_context() as session:
        # Find the task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise ValidationError(f"Task with ID {task_id} not found for user {user_id}")

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }


@tool(
    name="update_task",
    description="Update the title and/or description of a specific task for a user"
)
def update_task(user_id: int, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    Update the title and/or description of a specific task for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary with task update details
    """
    with get_session_context() as session:
        # Find the task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise ValidationError(f"Task with ID {task_id} not found for user {user_id}")

        # Update task fields if provided
        if title is not None and title.strip():
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description.strip() else None

        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }