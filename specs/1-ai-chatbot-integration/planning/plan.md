# Implementation Plan: AI Chatbot Integration

## Feature Overview
- **Feature**: AI Chatbot Integration for Todo App
- **Description**: Add a powerful AI chatbot that allows logged-in users to manage tasks via natural language
- **Branch**: feature/1-ai-chatbot-integration
- **Priority**: High

## Technical Context

### Known Information
- Frontend: Next.js 16+ (App Router) with Better Auth
- Backend: Python FastAPI + SQLModel + Neon PostgreSQL
- Authentication: Better Auth (JWT tokens)
- Database: Existing Task model with user_id ownership
- Technology Stack: OpenAI ChatKit, OpenAI Agents SDK (with Gemini compatibility), Official MCP SDK

### Unknown Information
- **Database connection details**: NEEDS CLARIFICATION
- **Gemini API key configuration and compatibility wrapper setup**: NEEDS CLARIFICATION
- **MCP SDK installation and configuration process**: NEEDS CLARIFICATION
- **Exact structure of existing Task model**: NEEDS CLARIFICATION
- **Better Auth JWT validation implementation details**: NEEDS CLARIFICATION

## Constitution Check

### Applied Principles from Project Constitution
- **Security First**: All implementations must validate user authentication and enforce data isolation
- **User Privacy**: User data must never be accessible to other users
- **Performance**: All operations should complete within acceptable timeframes
- **Modularity**: New features should be implemented as modular components
- **Documentation**: All new components must be documented

### Compliance Verification
- ✅ Will implement user authentication validation on all endpoints
- ✅ Will ensure data isolation between users
- ✅ Will maintain stateless server architecture
- ✅ Will provide proper error handling
- ✅ Will follow existing code patterns and conventions

### Gate Evaluation
- **All constitutional requirements satisfied**: PROCEED
- **No conflicts with established principles**: PROCEED
- **Security requirements addressed**: PROCEED

## Phase 0: Research & Discovery

### Research Tasks
1. **Database Connection Details Research**
   - Task: Research existing database connection patterns in the codebase
   - Outcome: Understanding of current database configuration

2. **OpenAI Integration Research**
   - Task: Research best practices for OpenAI integration with Python FastAPI
   - Outcome: Proper setup for OpenAI API usage

3. **MCP SDK Research**
   - Task: Research Official MCP SDK installation and configuration
   - Outcome: Understanding of tool creation patterns

4. **Authentication Validation Research**
   - Task: Research Better Auth JWT implementation details in existing codebase
   - Outcome: Proper authentication validation for new endpoints

5. **Task Model Structure Research**
   - Task: Examine existing Task model definition and structure
   - Outcome: Understanding of required fields and relationships

### Research Resolution Plan
All "NEEDS CLARIFICATION" items will be resolved through:
- Codebase exploration to understand existing patterns
- Documentation review for third-party services
- Configuration discovery from existing files

## Phase 1: Data Model & API Contracts

### Data Model Design

#### Conversation Entity
- **Fields**:
  - id (int, primary key, auto-increment)
  - user_id (str, foreign key to User)
  - created_at (datetime, default now)
  - updated_at (datetime, default now, auto-update)

#### Message Entity
- **Fields**:
  - id (int, primary key, auto-increment)
  - user_id (str, foreign key to User)
  - conversation_id (int, foreign key to Conversation)
  - role (str, enum: "user"|"assistant")
  - content (str, text content of message)
  - created_at (datetime, default now)

### API Contract Design

#### POST /api/{user_id}/chat
- **Authentication**: JWT Bearer token required
- **Path Parameters**: user_id (str)
- **Request Body**:
  ```json
  {
    "conversation_id": 123,
    "message": "Add task buy groceries"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": 123,
    "response": "Task 'buy groceries' created successfully",
    "tool_calls": []
  }
  ```
- **Status Codes**: 200 (success), 401 (unauthorized), 403 (forbidden), 500 (server error)

## Phase 2: Implementation Strategy

### Overall Sequence
1. Database schema & migrations first
2. MCP tools (the AI's "hands")
3. Backend chat endpoint + agent runner
4. AI agent configuration & system prompt
5. Frontend ChatKit integration
6. Testing, polish & documentation

### Phase 2A: Database Extensions
- Create Conversation & Message models
- Generate & apply database migration

### Phase 2B: MCP Tools Implementation
- Create MCP tools base structure
- Implement add_task, list_tasks, complete_task, delete_task, update_task tools
- Add common error handling & logging

### Phase 2C: Chat Endpoint & Conversation Logic
- Create chat router & endpoint skeleton
- Implement conversation fetch/create logic
- Load & format message history for agent
- Store user message before agent run
- Implement full agent runner call
- Store assistant response & tool metadata
- Return clean API response

### Phase 2D: AI Agent Configuration
- Create main Todo AI Agent definition
- Write strong system prompt
- Add example few-shot messages

### Phase 2E: Frontend ChatKit Integration
- Install & configure OpenAI ChatKit
- Create /chat page or component
- Wire ChatKit to backend endpoint
- Add loading, error & empty states

### Phase 2F: Testing & Polish
- Write basic manual test cases
- Add CORS, rate limiting
- Update README
- Final smoke test

## Phase 3: Risk Assessment

### High-Risk Areas
- User data isolation and authentication validation
- Third-party API integration (OpenAI, MCP SDK)
- Database migration and schema changes
- State management in stateless architecture

### Mitigation Strategies
- Comprehensive authentication checks on every endpoint
- Extensive error handling for API failures
- Database transaction safety for operations
- Proper environment configuration management

## Phase 4: Success Criteria
- All 25 planned tasks completed successfully
- End-to-end functionality verified
- Security requirements met (user isolation)
- Performance requirements satisfied (<3s response time)
- Proper error handling implemented