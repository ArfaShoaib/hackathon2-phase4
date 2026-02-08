# Manual Test Cases for AI Chatbot Integration

## Test Case 1: Task Creation via Chat
**Scenario**: User wants to add a new task using natural language
- **Given**: User is logged in and on the chat interface
- **When**: User sends message "Add task: Buy milk tomorrow"
- **Then**: System creates a task titled "Buy milk tomorrow" and responds "Task 'Buy milk tomorrow' has been created successfully."
- **Expected Tool Calls**: add_task with user_id and title parameters

## Test Case 2: Task Listing via Chat
**Scenario**: User wants to see their pending tasks
- **Given**: User has multiple tasks in their account
- **When**: User sends message "Show my pending tasks"
- **Then**: System lists all pending tasks for the user
- **Expected Tool Calls**: list_tasks with user_id and completed=False

## Test Case 3: Task Completion via Chat
**Scenario**: User wants to mark a task as completed
- **Given**: User has pending tasks including task #5
- **When**: User sends message "Complete task #5"
- **Then**: System marks task #5 as completed and confirms "Task #5 has been marked as completed."
- **Expected Tool Calls**: complete_task with user_id and task_id

## Test Case 4: Task Completion by Title
**Scenario**: User wants to complete a task by specifying its title
- **Given**: User has a pending task titled "Buy groceries"
- **When**: User sends message "Complete task 'Buy groceries'"
- **Then**: System marks the task as completed and confirms "Task 'Buy groceries' has been marked as completed."
- **Expected Tool Calls**: list_tasks (to find by title), complete_task with user_id and correct task_id

## Test Case 5: Task Deletion via Chat
**Scenario**: User wants to delete a task using its ID
- **Given**: User has a task with ID #3
- **When**: User sends message "Delete task #3"
- **Then**: System deletes task #3 and confirms "Task #3 has been deleted."
- **Expected Tool Calls**: delete_task with user_id and task_id

## Test Case 6: Task Deletion by Title
**Scenario**: User wants to delete a task by specifying its title
- **Given**: User has a task titled "Call plumber"
- **When**: User sends message "Delete the 'Call plumber' task"
- **Then**: System deletes the task and confirms "Task 'Call plumber' has been deleted."
- **Expected Tool Calls**: list_tasks (to find by title), delete_task with user_id and correct task_id

## Test Case 7: Task Update via Chat
**Scenario**: User wants to update a task title
- **Given**: User has a task titled "Buy groceries"
- **When**: User sends message "Change task 'Buy groceries' to 'Buy groceries and milk'"
- **Then**: System updates the task title and confirms "Task 'Buy groceries' has been updated to 'Buy groceries and milk'."
- **Expected Tool Calls**: list_tasks (to find by title), update_task with user_id, task_id, and new title

## Test Case 8: Authentication Validation - No JWT
**Scenario**: Unauthenticated user tries to access chat endpoint
- **Given**: User is not logged in
- **When**: User sends any message to the chat endpoint
- **Then**: System returns 401 Unauthorized error
- **Expected**: Error response with "Invalid authentication credentials"

## Test Case 9: Authentication Validation - Wrong User ID
**Scenario**: User tries to access another user's chat endpoint
- **Given**: User with ID 123 is logged in
- **When**: User accesses /api/456/chat endpoint with their own JWT
- **Then**: System returns 403 Forbidden error
- **Expected**: Error response with "Access denied: user ID mismatch"

## Test Case 10: Conversation Persistence
**Scenario**: User continues conversation across sessions
- **Given**: User has an existing conversation with ID 789
- **When**: User sends message with conversation_id 789
- **Then**: System continues the existing conversation and returns the same conversation_id
- **Expected**: Response includes conversation_id 789

## Test Case 11: New Conversation Creation
**Scenario**: User starts a new conversation
- **Given**: User is logged in and doesn't provide conversation_id
- **When**: User sends initial message to chat endpoint
- **Then**: System creates new conversation and returns new conversation_id
- **Expected**: Response includes new conversation_id and success message

## Test Case 12: Invalid Command Handling
**Scenario**: User sends an unrecognized command
- **Given**: User is logged in and on chat interface
- **When**: User sends message "What is the weather like?"
- **Then**: System responds with helpful guidance about available commands
- **Expected**: Response suggests available task management commands

## Test Case 13: Empty Task Title Handling
**Scenario**: User tries to add a task without specifying a title
- **Given**: User is logged in
- **When**: User sends message "Add task"
- **Then**: System responds with helpful error message
- **Expected**: Response "I couldn't identify the task title. Please specify what task you'd like to add."

## Test Case 14: Non-existent Task Operation
**Scenario**: User tries to operate on a task that doesn't exist
- **Given**: User is logged in
- **When**: User sends message "Complete task #999" (non-existent task)
- **Then**: System responds with appropriate error message
- **Expected**: Response "Task with ID 999 not found for user..."

## Test Case 15: Full Conversation Flow
**Scenario**: User performs multiple operations in a single conversation
- **Given**: User is logged in and starts a conversation
- **When**: User sequentially adds a task, lists tasks, completes a task, and deletes a task
- **Then**: All operations succeed and conversation maintains context
- **Expected**: Each operation produces expected responses and tool calls