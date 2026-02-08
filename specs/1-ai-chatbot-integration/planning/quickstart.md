# Quickstart Guide: AI Chatbot Integration

## Prerequisites

### Environment Setup
1. Ensure Python 3.9+ is installed
2. Ensure Node.js 18+ is installed (for frontend)
3. Obtain Google Gemini API key
4. Ensure access to Neon PostgreSQL database
5. Verify Better Auth is properly configured

### Required Packages
```bash
# Backend dependencies
pip install fastapi sqlmodel python-multipart python-jose[cryptography] python-dotenv

# OpenAI SDK (for compatibility layer) and MCP SDK
pip install openai openai-mcp

# Google Gemini API client
pip install google-generativeai

# Gemini compatibility wrapper for OpenAI SDK (if needed)
pip install openai-gemini-adapter  # or similar compatibility layer

# Frontend dependencies (to be added to existing Next.js project)
npm install @openai/chat-components-react
```

## Implementation Steps

### Step 1: Database Setup
1. Create the Conversation and Message models in your models directory
2. Generate and apply the database migration
3. Verify the tables exist in your database

### Step 2: MCP Tools Implementation
1. Create the MCP tools directory structure
2. Implement the five required tools:
   - add_task
   - list_tasks
   - complete_task
   - delete_task
   - update_task
3. Test each tool individually

### Step 3: Backend Chat Endpoint
1. Create the chat router with the protected endpoint
2. Implement conversation fetch/create logic
3. Implement message history loading
4. Store user messages before agent processing
5. Connect to the AI agent with tools
6. Store assistant responses
7. Return clean responses

### Step 4: AI Agent Configuration
1. Create the main AI agent instance
2. Define the system prompt with proper rules
3. Attach the MCP tools to the agent
4. Test the agent with sample inputs

### Step 5: Frontend Integration
1. Install OpenAI ChatKit
2. Create the chat page/component
3. Connect to the backend endpoint
4. Handle conversation persistence
5. Add error/loading states

## Environment Variables

### Backend (.env)
```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key_from_openai_allowlist
NEXT_PUBLIC_CHAT_BACKEND_URL=https://your-backend-url.com
```

## Testing Scenarios

### Manual Test Cases
1. **Task Creation**: Send "Add task: Buy milk" → Verify task created
2. **Task Listing**: Send "Show my pending tasks" → Verify correct tasks returned
3. **Task Completion**: Send "Complete task #1" → Verify task marked complete
4. **Task Deletion**: Send "Delete task 'Buy groceries'" → Verify task deleted
5. **Task Update**: Send "Change task 'Old title' to 'New title'" → Verify update

### Authentication Tests
1. Try accessing without JWT → Should return 401
2. Try accessing with wrong user_id → Should return 403
3. Try accessing with valid JWT and correct user_id → Should succeed

## Common Issues and Solutions

### Issue: MCP SDK not installing
**Solution**: Check the official MCP SDK documentation for the correct installation command

### Issue: Gemini API returning rate limit errors
**Solution**: Implement retry logic with exponential backoff

### Issue: JWT validation failing
**Solution**: Verify the JWT token format and secret key match between frontend and backend

### Issue: CORS errors
**Solution**: Configure CORS middleware in FastAPI to allow your frontend domain

## Development Commands

### Backend
```bash
# Run the backend server
uvicorn main:app --reload

# Run database migrations
python -m alembic upgrade head
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

## Security Considerations
- Never log JWT tokens or other sensitive information
- Validate all user inputs to prevent injection attacks
- Ensure all database queries are parameterized
- Implement rate limiting to prevent abuse
- Verify user ownership of resources before operations