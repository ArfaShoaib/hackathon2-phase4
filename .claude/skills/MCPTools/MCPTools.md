# MCP Tools Skill

## Overview
This skill designs, implements and maintains all MCP tools that give the AI agent power to manage user's tasks securely, implementing 5 core task management functions.

## Responsibilities
- Implement 5 core MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Enforce strict user_id validation in every tool (must match authenticated user)
- Return consistent structured JSON responses ({task_id, status, title, ...})
- Add input validation, error handling and friendly error objects
- Support optional filters/sorting in list_tasks (status, search, limit)
- Allow future extension (e.g. priority, due_date fields)
- Document tool schemas clearly for the AI agent to understand

## Key Functions

### 1. Core Task Operations
- Implement add_task: Create new tasks with validation and user association
- Implement list_tasks: Retrieve tasks with optional filters and sorting
- Implement complete_task: Update task status with validation
- Implement delete_task: Remove tasks with proper authorization checks
- Implement update_task: Modify task properties safely

### 2. User Validation and Security
- Enforce strict user_id validation in every tool
- Ensure operations only affect current user's tasks
- Prevent access to other users' data
- Implement proper authentication checks

### 3. Data Validation and Error Handling
- Add comprehensive input validation for all tools
- Return friendly error objects with clear messages
- Handle edge cases and invalid inputs gracefully
- Maintain data integrity across operations

### 4. Response Standardization
- Return consistent structured JSON responses
- Include appropriate metadata (task_id, status, title, etc.)
- Format responses for easy consumption by AI agent
- Maintain response format consistency across all tools

### 5. Advanced Features
- Support optional filters and sorting in list_tasks
- Enable pagination and limits for large datasets
- Allow future extensions (priority, due_date fields)
- Provide clear tool documentation and schemas

## Technical Requirements
- Built with Official MCP SDK
- Uses SQLModel for database interactions
- Implements FastAPI dependency injection
- Connects to Neon PostgreSQL database
- Ensures atomic and safe operations

## Constraints
- Tools must be completely stateless
- No direct OpenAI / agent runner logic
- Never return sensitive data (e.g. other users' tasks)
- All operations must be atomic and safe (use transactions where needed)
- Maintain user data isolation at all times
- Follow established API patterns and conventions