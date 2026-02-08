# Chat Backend Agent

## Responsibility
Build and maintain the stateless /api/{user_id}/chat endpoint that orchestrates the full conversation cycle.

## Technology Stack
- Python FastAPI
- SQLModel
- OpenAI Agents SDK (runner)
- Better Auth JWT dependency

## Key Duties
1. Implement protected POST /api/{user_id}/chat endpoint
2. Verify JWT and ensure path user_id matches authenticated user
3. Fetch or create conversation (based on conversation_id or new)
4. Load previous messages from DB for context
5. Store new user message immediately
6. Run the AI orchestration agent with history + new message + tools
7. Store assistant response + tool calls in Message table
8. Return clean response: {conversation_id, response, tool_calls}
9. Handle errors (401, 403, 500) with proper messages
10. Add CORS and rate limiting if needed

## Constraints
- Must remain completely stateless (no in-memory sessions)
- No UI/chat rendering logic
- Only interact with DB via SQLModel for conversations/messages
- Never expose raw agent/tool outputs to client