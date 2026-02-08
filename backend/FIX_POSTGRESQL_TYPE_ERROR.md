# PostgreSQL Type Mismatch Fix

## Problem
The application was encountering the following PostgreSQL error:
```
operator does not exist: character varying = integer
LINE 3: WHERE conversation.id = 4 AND conversation.user_id = 1
```

This occurred because the `conversation.id` column in the database was defined as VARCHAR, but the SQLModel definition expected an INTEGER.

## Solution

### 1. Runtime Fix
The immediate fix implemented type casting in SQL queries to handle the mismatch:

- Updated `get_or_create_conversation()` function to use `cast(Conversation.id, Integer)` in queries
- Created utility functions in `utils/db_utils.py` to handle casting consistently
- Applied casting to both conversation and message queries

### 2. Permanent Fix
Created a migration script to permanently fix the database schema:

- `migrate_conversation_id.py` - Converts VARCHAR columns to INTEGER
- Updates both `conversation.id` and `message.conversation_id` columns
- Handles PostgreSQL-specific syntax for type conversion

## How to Apply the Fix

### Option 1: Run the Migration Script (Recommended)
```bash
cd backend
python migrate_conversation_id.py
```

This will:
- Change `conversation.id` from VARCHAR to INTEGER
- Change `message.conversation_id` from VARCHAR to INTEGER
- Maintain all existing data

### Option 2: Continue with Runtime Casting (Temporary)
The application will continue to work with the runtime casting fix, but it's recommended to run the migration for better performance.

## Files Modified
- `agents/todo_agent.py` - Updated queries with casting
- `utils/db_utils.py` - Added casting utility functions
- `models/conversation.py` - Maintained INTEGER type definition
- `migrate_conversation_id.py` - Database migration script

## Notes
- The SQLModel definition expects INTEGER primary keys (best practice)
- The migration ensures the database schema matches the model definition
- After migration, the casting becomes unnecessary but harmless