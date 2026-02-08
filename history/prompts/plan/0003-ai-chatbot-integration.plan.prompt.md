---
id: "0003"
title: "AI Chatbot Integration Plan"
stage: "plan"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-chatbot-integration"
branch: "main"
user: "user"
command: "/sp.plan"
labels: ["ai", "chatbot", "planning", "database", "mcp-tools", "api-contracts"]
links:
  spec: "../spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "specs/1-ai-chatbot-integration/planning/plan.md"
  - "specs/1-ai-chatbot-integration/planning/research.md"
  - "specs/1-ai-chatbot-integration/planning/data-model.md"
  - "specs/1-ai-chatbot-integration/planning/contracts/chat-api.yaml"
  - "specs/1-ai-chatbot-integration/planning/quickstart.md"
tests_yaml:
  - "none"
---

# Prompt History Record

## Original Prompt Text

# /sp.plan

**Project**: Todo Full-Stack Multi-User Web Application – Phase III (AI Chatbot Integration)
**Goal of this plan**: Break the implementation of the AI Chatbot (natural language task management) into small, sequential, clearly defined tasks that follow the Agentic Dev Stack workflow.

**Overall Sequence Reminder**
1. Database schema & migrations first
2. MCP tools (the AI's "hands")
3. Backend chat endpoint + agent runner
4. AI agent configuration & system prompt
5. Frontend ChatKit integration
6. Testing, polish & documentation

**Phase 1 – Database Extensions**
1. **Create Conversation & Message models**
   - File: `models/conversation.py` and `models/message.py`
   - Define SQLModel classes with proper fields, foreign keys to User/Task, timestamps
   - Acceptance: models compile, no syntax errors

2. **Generate & apply database migration**
   - Use Alembic or manual SQLModel metadata.create_all()
   - Add Conversation and Message tables
   - Acceptance: tables appear in Neon DB (check via pgAdmin / psql)

**Phase 2 – MCP Tools Implementation**
3. **Create MCP tools base structure**
   - Folder: `mcp/tools/`
   - Create base tool class or decorator using Official MCP SDK
   - Acceptance: empty tool skeleton runs without crash

4. **Implement add_task MCP tool**
   - Validate user_id, title length, optional description
   - Create Task in DB, return structured JSON
   - Handle duplicate titles warning (optional)
   - Acceptance: tool can be called manually and creates task

5. **Implement list_tasks MCP tool**
   - Filter by status (all/pending/completed), default "all"
   - Return clean list of task objects (no sensitive fields)
   - Acceptance: returns correct filtered list for given user_id

6. **Implement complete_task, delete_task, update_task tools**
   - Each: check ownership, update/delete, return status JSON
   - 404-style error if task not found or wrong owner
   - Acceptance: each tool works independently via test call

7. **Add common error handling & logging to all tools**
   - Consistent error format: {"error": str, "code": int}
   - Optional: log tool calls (print or structured logger)
   - Acceptance: invalid input → nice error, not crash

**Phase 3 – Chat Endpoint & Conversation Logic**
8. **Create chat router & endpoint skeleton**
   - File: `routers/chat.py`
   - POST /api/{user_id}/chat
   - Add JWT dependency, validate user_id match
   - Acceptance: endpoint returns 401/403 on bad auth

9. **Implement conversation fetch / create logic**
   - If conversation_id given → load, else create new Conversation
   - Acceptance: new conversation created on first message

10. **Load & format message history for agent**
    - Query Messages by conversation_id, order by created_at
    - Convert to OpenAI-compatible message list (role + content)
    - Acceptance: history correctly formatted

11. **Store user message before agent run**
    - Insert Message with role="user" immediately after receiving
    - Acceptance: message saved even if agent fails later

12. **Implement full agent runner call**
    - Pass history + new message + all MCP tools to OpenAI Agent
    - Capture response + tool calls
    - Acceptance: dummy agent returns something

13. **Store assistant response & tool metadata**
    - Save assistant message + any tool_call info
    - Acceptance: DB shows full round-trip

14. **Return clean API response**
    - {conversation_id, response, tool_calls}
    - Handle agent errors gracefully (500 with message)
    - Acceptance: curl/postman returns expected format

**Phase 4 – AI Agent Configuration**
15. **Create main Todo AI Agent definition**
    - File: `agents/todo_agent.py`
    - Attach all 5 MCP tools
    - Set model (e.g. gpt-4o-mini or gpt-4o)
    - Acceptance: agent initializes

16. **Write strong system prompt**
    - Friendly, confirmatory, bilingual (English + Urdu/Hinglish)
    - Rules: confirm deletes, chain tools, refuse off-topic
    - Acceptance: prompt is saved as constant / file

17. **Add example few-shot messages (optional but recommended)**
    - Help agent learn desired response style
    - Acceptance: prompt includes 3–5 good/bad examples

**Phase 5 – Frontend ChatKit Integration**
18. **Install & configure OpenAI ChatKit**
    - Add dependency, get domain key (allowlist done)
    - Acceptance: basic ChatKit renders on page

19. **Create /chat page or component**
    - Protected route (redirect if not logged in)
    - Pass user_id and JWT to ChatKit
    - Acceptance: chat UI visible for logged-in user

20. **Wire ChatKit to backend endpoint**
    - On send → POST to /api/{user_id}/chat
    - Handle conversation_id persistence (localStorage)
    - Display streaming / final response
    - Acceptance: message sent → AI reply appears

21. **Add loading, error & empty states**
    - Show spinner, "No internet", "Please login", etc.
    - Acceptance: good UX on failures

**Phase 6 – Testing & Polish**
22. **Write basic manual test cases**
    - Add task via "add buy milk"
    - List pending tasks
    - Delete with confirmation flow
    - Resume old conversation
    - Acceptance: documented checklist

23. **Add CORS, rate limiting (if needed)**
    - Ensure frontend origin allowed
    - Optional: basic rate limit on /chat
    - Acceptance: no CORS errors in browser

24. **Update README**
    - How to run chatbot
    - OpenAI key & domain allowlist steps
    - Acceptance: new section added

25. **Final smoke test**
    - Login → go to chat → 5 different natural commands → verify DB & UI
    - Acceptance: end-to-end working

**Estimated task count**: 25 small steps
**Next action**: Start implementing from task 1, one by one.
Use Claude Code / your agent with prompts like:
"Implement task 4 as MCP Tools Agent"

```

## Response Summary

Updated comprehensive implementation plan for AI Chatbot Integration to use Google's Gemini API instead of OpenAI API while maintaining the OpenAI Agents SDK framework:
- Updated planning document to reflect Gemini API integration with OpenAI SDK compatibility
- Updated research findings to address Gemini API with compatibility wrapper approach
- Updated data model specification for Conversation and Message entities
- Updated API contract specification in OpenAPI format
- Updated quickstart guide with Gemini API implementation steps and testing scenarios
- Added Gemini integration guide documenting the compatibility layer approach

## Outcome and Impact

Developed complete planning foundation for the AI chatbot implementation with all necessary technical specifications and architectural decisions documented. The plan addresses security, scalability, and integration requirements while maintaining the existing technology stack.

## Files Modified

- specs/1-ai-chatbot-integration/planning/plan.md
- specs/1-ai-chatbot-integration/planning/research.md
- specs/1-ai-chatbot-integration/planning/data-model.md
- specs/1-ai-chatbot-integration/planning/contracts/chat-api.yaml
- specs/1-ai-chatbot-integration/planning/quickstart.md
- specs/1-ai-chatbot-integration/planning/gemini-integration-guide.md

## Tests Summary

None

## Next Steps

- Begin implementation following the phased approach outlined in the plan
- Start with database extensions (Conversation and Message models)
- Proceed through MCP tools implementation
- Continue with backend and frontend integration
- Complete testing and documentation

## Reflection

The planning phase has established a solid foundation with clear specifications for the entire AI chatbot integration project. All technical unknowns have been researched and resolved, providing clear direction for implementation.