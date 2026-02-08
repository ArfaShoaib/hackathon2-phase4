# Chat Backend Skill

## Overview
This skill manages the backend API endpoints for the AI chatbot, handling authentication verification, conversation management, and orchestration of AI interactions with MCP tools.

## Responsibilities
- Implement protected POST /api/{user_id}/chat endpoint
- Verify JWT tokens and authenticate user identity
- Manage conversation state (fetch/create based on conversation_id)
- Load and store conversation history in database
- Orchestrate AI agent with tools and message history
- Handle errors and return appropriate responses

## Key Functions

### 1. Authentication Verification
- Verify JWT token from incoming requests
- Ensure path user_id matches authenticated user
- Return 401/403 errors for invalid authentication
- Extract user context from JWT claims

### 2. Conversation Management
- Fetch existing conversation by conversation_id
- Create new conversation if none exists
- Load previous messages from database for context
- Maintain conversation statelessness

### 3. Message Handling
- Store new user messages immediately in database
- Retrieve assistant responses and tool calls
- Manage message history for AI context
- Return clean responses with conversation_id

### 4. AI Orchestration
- Run AI orchestration agent with message history
- Integrate MCP tools for task management
- Process tool calls and return results
- Format responses for frontend consumption

### 5. Error Handling and Security
- Implement proper error responses (401, 403, 500)
- Ensure user isolation (users can't access others' data)
- Apply rate limiting and CORS policies
- Maintain stateless operation (no in-memory sessions)

## Technical Requirements
- Built with Python FastAPI
- Uses SQLModel for database interactions
- Integrates OpenAI Agents SDK for AI orchestration
- Implements Better Auth JWT dependency
- Stateless operation with no in-memory sessions

## Constraints
- Must remain completely stateless (no in-memory sessions)
- No direct UI/chat rendering logic
- Only interact with DB via SQLModel for conversations/messages
- Never expose raw agent/tool outputs to client
- All operations must be atomic and secure