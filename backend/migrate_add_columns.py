"""
Migration script to add answer_details and ethical_bias_summary columns to quiz_attempts table.
Run this script once to update your existing database schema.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import JSONB

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

def migrate():
    """Add missing columns to quiz_attempts table"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.begin() as conn:
        # Check if columns already exist
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'quiz_attempts' 
            AND column_name IN ('answer_details', 'ethical_bias_summary')
        """)
        result = conn.execute(check_query)
        existing_columns = [row[0] for row in result]
        
        # Add answer_details column if it doesn't exist
        if 'answer_details' not in existing_columns:
            print("Adding answer_details column...")
            conn.execute(text("""
                ALTER TABLE quiz_attempts 
                ADD COLUMN answer_details JSONB DEFAULT '{}'::jsonb
            """))
            # Set default for existing rows
            conn.execute(text("""
                UPDATE quiz_attempts 
                SET answer_details = '{}'::jsonb 
                WHERE answer_details IS NULL
            """))
            print("✓ Added answer_details column")
        else:
            print("✓ answer_details column already exists")
        
        # Add ethical_bias_summary column if it doesn't exist
        if 'ethical_bias_summary' not in existing_columns:
            print("Adding ethical_bias_summary column...")
            conn.execute(text("""
                ALTER TABLE quiz_attempts 
                ADD COLUMN ethical_bias_summary TEXT
            """))
            print("✓ Added ethical_bias_summary column")
        else:
            print("✓ ethical_bias_summary column already exists")
        
        # Create user_justifications table if it doesn't exist
        check_table = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'user_justifications'
            )
        """)
        table_exists = conn.execute(check_table).scalar()
        
        if not table_exists:
            print("Creating user_justifications table...")
            conn.execute(text("""
                CREATE TABLE user_justifications (
                    id SERIAL PRIMARY KEY,
                    attempt_id INTEGER NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
                    question_id INTEGER NOT NULL,
                    justification_text TEXT,
                    user_answer VARCHAR,
                    is_correct INTEGER DEFAULT 0,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("✓ Created user_justifications table")
        else:
            print("✓ user_justifications table already exists")
        
        print("\nMigration completed successfully!")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"Error during migration: {e}")
        raise

