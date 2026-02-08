# Chatbot UI Skill

## Overview
This skill handles the user interface for the AI chatbot, integrating OpenAI ChatKit with the Next.js frontend and managing user authentication via Better Auth.

## Responsibilities
- Initialize and configure the ChatKit component
- Handle user authentication state and JWT token management
- Manage conversation persistence and history
- Display loading states and error messages appropriately
- Support bilingual interface (English + Urdu/Hinglish)

## Key Functions

### 1. Component Integration
- Integrate ChatKit component into designated route (/chat or /ai)
- Configure component with user authentication data
- Set up proper event handlers and callbacks

### 2. Authentication Management
- Retrieve user_id and JWT from Better Auth
- Pass authentication data securely to ChatKit
- Handle authentication failures gracefully

### 3. Conversation Handling
- Implement conversation_id persistence (localStorage/session)
- Resume existing conversations when possible
- Start new conversations based on user preference
- Maintain chat history display

### 4. User Experience Features
- Display appropriate loading states during AI responses
- Show friendly error messages ('Please login first', 'Something went wrong')
- Implement bilingual UI text support
- Ensure responsive design for different screen sizes

## Technical Requirements
- Built with Next.js 16+ (App Router)
- Uses OpenAI ChatKit for chat interface
- Integrates with Better Auth for authentication
- Secure handling of JWT tokens
- No direct database queries allowed

## Constraints
- Must only communicate with backend via /api/{user_id}/chat endpoint
- Never expose JWT secrets or backend URLs in client-side code
- No direct database queries from UI component
- No MCP tool definitions in UI code