#!/usr/bin/env python3
"""
Migration script to fix the conversation.id column type from VARCHAR to INTEGER
to match the SQLModel definition.
"""

import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, select
from models.conversation import Conversation
from models.message import Message

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

def migrate_conversation_id_type():
    """
    Migrate the conversation.id column from VARCHAR to INTEGER
    """
    # Check if we're using PostgreSQL
    if DATABASE_URL.startswith("postgresql://"):
        print("Detected PostgreSQL database, performing migration...")
        
        # Connect directly to the database to execute ALTER TABLE
        import psycopg2
        from urllib.parse import urlparse
        
        # Parse the database URL
        parsed = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
        cur = conn.cursor()
        
        try:
            # First, check the current column type
            cur.execute("""
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = 'conversation' AND column_name = 'id';
            """)
            current_type = cur.fetchone()[0]
            print(f"Current conversation.id column type: {current_type}")
            
            if current_type.lower() != 'integer':
                # Perform the ALTER TABLE to change the column type
                print("Changing conversation.id column type to INTEGER...")
                cur.execute("""
                    ALTER TABLE conversation ALTER COLUMN id TYPE INTEGER USING (id::INTEGER);
                """)
                print("Updated conversation.id column type to INTEGER")
            
            # Also update the foreign key in messages table
            cur.execute("""
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = 'message' AND column_name = 'conversation_id';
            """)
            msg_current_type = cur.fetchone()[0]
            print(f"Current message.conversation_id column type: {msg_current_type}")
            
            if msg_current_type.lower() != 'integer':
                print("Updating message.conversation_id column type to INTEGER...")
                cur.execute("""
                    ALTER TABLE message ALTER COLUMN conversation_id TYPE INTEGER USING (conversation_id::INTEGER);
                """)
                print("Updated message.conversation_id column type to INTEGER")
            
            # Update the sequence if it exists (for auto-increment)
            cur.execute("""
                SELECT sequence_name FROM information_schema.columns 
                WHERE table_name = 'conversation' AND column_name = 'id' 
                AND is_identity = 'YES';
            """)
            
            seq_result = cur.fetchone()
            if seq_result:
                sequence_name = seq_result[0]
                print(f"Updating sequence {sequence_name}...")
                cur.execute(f"ALTER SEQUENCE {sequence_name} AS INTEGER;")
            
            conn.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
    else:
        print("Database is not PostgreSQL, migration script is specific to PostgreSQL")
        return False

    return True

if __name__ == "__main__":
    success = migrate_conversation_id_type()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        exit(1)