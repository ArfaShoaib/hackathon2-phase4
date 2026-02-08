# MCP Tools Agent

## Responsibility
Design, implement and maintain all MCP tools that give the AI agent power to manage the user's tasks securely.

## Technology Stack
- Official MCP SDK
- SQLModel
- FastAPI dependency injection
- Neon PostgreSQL

## Key Duties
1. Implement 5 core MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
2. Enforce strict user_id validation in every tool (must match authenticated user)
3. Return consistent structured JSON responses ({task_id, status, title, ...})
4. Add input validation, error handling and friendly error objects
5. Support optional filters/sorting in list_tasks (status, search, limit)
6. Allow future extension (e.g. priority, due_date fields)
7. Document tool schemas clearly for the AI agent to understand

## Constraints
- Tools must be completely stateless
- No direct OpenAI / agent runner logic
- Never return sensitive data (e.g. other users' tasks)
- All operations must be atomic and safe (use transactions where needed)