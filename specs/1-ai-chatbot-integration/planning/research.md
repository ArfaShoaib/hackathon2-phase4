# Research Findings: AI Chatbot Integration

## Database Connection Details

### Decision
Use the existing SQLModel and Neon PostgreSQL connection pattern already established in the codebase.

### Rationale
Following existing patterns ensures consistency and reduces potential integration issues. Since the backend already uses SQLModel with Neon PostgreSQL, we should leverage the same connection pool and configuration approach.

### Alternatives Considered
- Alternative ORM frameworks: Would create inconsistency with existing codebase
- Different database systems: Would complicate the architecture unnecessarily

## Gemini API Integration with OpenAI SDK Compatibility

### Decision
Use Google's Gemini API with a compatibility wrapper that allows OpenAI Agents SDK to interface with Gemini's API.

### Rationale
Using Gemini API while maintaining the OpenAI Agents SDK framework allows leveraging Gemini's capabilities while keeping the familiar SDK interface. This requires a compatibility layer that maps OpenAI SDK calls to Gemini API equivalents.

### Implementation Pattern
- Use GOOGLE_GEMINI_API_KEY environment variable
- Implement or use an existing OpenAI-Gemini compatibility wrapper
- Map OpenAI Agent calls to Gemini API equivalents
- Use Gemini Pro (gemini-pro) model for balanced performance/cost

## MCP SDK Installation and Configuration

### Decision
Install the Official MCP SDK via pip and implement tools using the decorator pattern for simplicity.

### Rationale
Using the official SDK ensures compatibility and access to the latest features. The decorator pattern makes tool creation and management cleaner.

### Implementation Pattern
- Install with `pip install openai-mcp`
- Create tools using `@tool` decorator
- Include proper type hints and error handling

## Better Auth JWT Validation

### Decision
Use the existing Better Auth JWT validation pattern from the current backend implementation.

### Rationale
Leveraging existing authentication infrastructure ensures consistency and avoids potential security vulnerabilities from implementing custom validation.

### Implementation Pattern
- Import existing JWT validation middleware/function
- Verify token authenticity
- Compare user_id in token with user_id in URL path
- Return 401/403 for invalid requests

## Existing Task Model Structure

### Research Outcome
Based on typical task management applications, the existing Task model likely includes:
- id (primary key)
- user_id (foreign key for ownership)
- title (task title)
- description (optional task description)
- completed (boolean for completion status)
- created_at and updated_at (timestamps)

### Implementation Assumption
We'll design MCP tools to work with these standard fields, adapting as needed once the actual structure is confirmed.

## Architecture Patterns

### Decision
Maintain stateless server architecture while persisting conversation state in the database.

### Rationale
Stateless architecture enables better scalability and reliability. Database persistence ensures conversation continuity without server-side state storage.

### Implementation Pattern
- Store conversation context in Conversation and Message tables
- Load context from DB before each AI interaction
- Save responses back to DB after AI processing