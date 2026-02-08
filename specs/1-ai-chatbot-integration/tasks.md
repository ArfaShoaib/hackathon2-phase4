# Tasks: AI Chatbot Integration

## Feature: AI Chatbot Integration for Todo App
**Goal**: Add a powerful AI chatbot that allows logged-in users to manage tasks via natural language

## Phase 1: Setup Tasks
- [X] T001 Install required packages for OpenAI-Gemini compatibility layer in backend requirements.txt
- [X] T002 Install Google Generative AI library via pip install google-generativeai
- [X] T003 Install OpenAI library and MCP SDK via pip install openai openai-mcp
- [X] T004 Create project directory structure for models (models/) and routers (routers/)
- [X] T005 Set up environment variables for GOOGLE_GEMINI_API_KEY in .env file
- [X] T006 Configure development environment with required dependencies

## Phase 2: Foundational Tasks
- [X] T007 Create Conversation model class in models/conversation.py with user_id, created_at, updated_at fields
- [X] T008 Create Message model class in models/message.py with user_id, conversation_id, role, content, created_at fields
- [X] T009 Generate and apply database migration for Conversation and Message tables
- [X] T010 Create MCP tools base structure in mcp/tools/__init__.py with base decorator/class
- [X] T011 Implement user authentication validation utility in utils/auth.py for JWT verification
- [X] T012 Create shared error handling module in utils/errors.py with consistent error format

## Phase 3: MCP Tools Implementation [US1]
- [X] T013 [US1] Implement add_task MCP tool in mcp/tools/task_operations.py with user_id validation
- [X] T014 [US1] Implement list_tasks MCP tool in mcp/tools/task_operations.py with status filtering
- [X] T015 [US1] Implement complete_task MCP tool in mcp/tools/task_operations.py with ownership check
- [X] T016 [US1] Implement delete_task MCP tool in mcp/tools/task_operations.py with ownership validation
- [X] T017 [US1] Implement update_task MCP tool in mcp/tools/task_operations.py with user validation
- [X] T018 [US1] Add common error handling and logging to all MCP tools in mcp/tools/error_handling.py

## Phase 4: Chat Endpoint Implementation [US2]
- [X] T019 [US2] Create chat router skeleton in routers/chat.py with JWT dependency
- [X] T020 [US2] Implement POST /api/{user_id}/chat endpoint with authentication validation
- [X] T021 [US2] Implement conversation fetch/create logic in routers/chat.py
- [X] T022 [US2] Implement message history loading and formatting in routers/chat.py
- [X] T023 [US2] Implement user message storage before agent processing in routers/chat.py
- [X] T024 [US2] Connect OpenAI-Gemini compatibility layer to router in routers/chat.py

## Phase 5: AI Agent Configuration [US3]
- [X] T025 [US3] Create main Todo AI Agent definition in agents/todo_agent.py
- [X] T026 [US3] Configure OpenAI-Gemini compatibility wrapper to use Google API
- [X] T027 [US3] Attach all 5 MCP tools to the AI agent in agents/todo_agent.py
- [X] T028 [US3] Write strong system prompt in prompts/todo_agent_system_prompt.txt
- [X] T029 [US3] Add example few-shot messages to prompts/examples.txt for agent training
- [X] T030 [US3] Implement response formatting for bilingual support (English + Urdu/Hinglish)

## Phase 6: Backend Integration [US4]
- [X] T031 [US4] Implement full agent runner call in routers/chat.py with history and tools
- [X] T032 [US4] Store assistant response and tool metadata in Message table in routers/chat.py
- [X] T033 [US4] Return clean API response with {conversation_id, response, tool_calls} format
- [X] T034 [US4] Add error handling for agent failures in routers/chat.py
- [X] T035 [US4] Implement proper response streaming to frontend in routers/chat.py
- [X] T036 [US4] Add rate limiting and CORS configuration to chat endpoint

## Phase 7: Frontend ChatKit Integration [US5]
- [X] T037 [US5] Install OpenAI ChatKit in frontend with npm install @openai/chat-components-react
- [X] T038 [US5] Create /chat page component in frontend app/chat/page.tsx
- [X] T039 [US5] Implement authentication guard to redirect non-logged-in users in app/chat/page.tsx
- [X] T040 [US5] Pass user_id and JWT to ChatKit configuration in app/chat/page.tsx
- [X] T041 [US5] Configure ChatKit to connect to backend endpoint /api/{user_id}/chat
- [X] T042 [US5] Implement conversation_id persistence in localStorage in app/chat/page.tsx

## Phase 8: Frontend Enhancement [US6]
- [X] T043 [US6] Add loading states to ChatKit component in app/chat/page.tsx
- [X] T044 [US6] Add error handling and friendly error messages in app/chat/page.tsx
- [X] T045 [US6] Implement empty state for new conversations in app/chat/page.tsx
- [X] T046 [US6] Add bilingual UI text support (English + Urdu/Hinglish) in app/chat/page.tsx
- [X] T047 [US6] Handle conversation resumption and history display in app/chat/page.tsx
- [X] T048 [US6] Add proper UX for different error scenarios in app/chat/page.tsx

## Phase 9: Polish & Cross-Cutting Concerns
- [X] T049 Add comprehensive logging throughout the chat system in utils/logging.py
- [X] T050 Write basic manual test cases in docs/manual_test_cases.md
- [X] T051 Update README with new chatbot feature instructions in README.md
- [X] T052 Add OpenAI key and domain allowlist setup instructions to README.md
- [X] T053 Perform final end-to-end smoke test with 5 different natural commands
- [X] T054 Optimize database queries for message history loading in routers/chat.py

## Dependencies
- Task T007-T009 must complete before T013-T018 (Models needed for MCP tools)
- Task T010 must complete before T013-T018 (Base structure for MCP tools)
- Task T013-T018 must complete before T025-T030 (Tools needed for agent)
- Task T007-T009 must complete before T019-T024 (DB schema for chat endpoint)
- Task T025-T030 must complete before T031-T036 (Agent needed for backend integration)
- Task T019-T036 must complete before T037-T042 (Backend needed for frontend integration)

## Parallel Execution Opportunities
- Tasks T007 and T008 can run in parallel (separate model files)
- Tasks T013-T017 can run in parallel (separate MCP tools)
- Tasks T037-T042 can run in parallel with Tasks T031-T036 (frontend/backend in parallel)
- Tasks T043-T048 can run in parallel with Tasks T025-T030 (frontend improvements)

## Implementation Strategy
**MVP Scope**: Complete Phase 1-4 to have a working chat endpoint with basic task operations
**Incremental Delivery**: Each user story phase delivers a complete, testable feature
**Testing Strategy**: Manual test cases for each user story before moving to next phase