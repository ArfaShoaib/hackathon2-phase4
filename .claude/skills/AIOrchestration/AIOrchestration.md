# AI Orchestration Skill

## Overview
This skill configures and runs the OpenAI Agent that interprets natural language and decides which MCP tools to call, managing the core AI logic for task management operations.

## Responsibilities
- Create and configure the main Todo AI agent with strong system prompt
- Attach all 5 MCP tools to the agent (add_task, list_tasks, complete_task, delete_task, update_task)
- Define behavior rules for confirmation before delete/complete operations
- Handle multi-turn reasoning and tool chaining when needed
- Support bilingual responses (English + Urdu/Hinglish)
- Format final responses to be human-friendly with action confirmations

## Key Functions

### 1. Agent Configuration
- Set up OpenAI Agent with appropriate system prompt
- Configure agent parameters for optimal task management
- Define agent behavior and response patterns
- Implement bilingual support for English and Urdu/Hinglish

### 2. Tool Integration
- Attach all 5 MCP tools to the agent (add_task, list_tasks, complete_task, delete_task, update_task)
- Ensure proper tool schema definitions
- Handle tool call responses and errors
- Validate tool parameters and inputs

### 3. Natural Language Processing
- Interpret user requests in natural language
- Map user intents to appropriate MCP tools
- Handle ambiguous input gracefully
- Support multi-turn conversations for complex operations

### 4. Behavior Rules Implementation
- Implement confirmation prompts before delete/complete operations
- Chain tools when needed for complex operations
- Handle off-topic questions appropriately
- Maintain conversation context across multiple exchanges

### 5. Response Formatting
- Format agent responses to be human-friendly
- Include action confirmations for completed operations
- Provide clear feedback for all user interactions
- Ensure responses align with user's language preference

## Technical Requirements
- Built with OpenAI Agents SDK
- Integrates with MCP SDK for tool access
- Uses Better Auth JWT claims for user context
- Maintains user isolation (operates only on current user's tasks)
- Follows established conversation patterns

## Constraints
- No UI or frontend code
- No direct database operations (only via MCP tools)
- Must not invent tools or capabilities that don't exist
- Ensure agent only operates on current user's tasks
- Maintain security and user data isolation
- Follow established system prompt guidelines