"""
Migration script to:
1. Create ethical_bias_profiles table
2. Remove ethical_bias_summary column from quiz_attempts table

Run this script once to update your existing database schema.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

def migrate():
    """Migrate ethical bias profile to separate table"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.begin() as conn:
        # 1. Create ethical_bias_profiles table if it doesn't exist
        check_table = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'ethical_bias_profiles'
            )
        """)
        table_exists = conn.execute(check_table).scalar()
        
        if not table_exists:
            print("Creating ethical_bias_profiles table...")
            conn.execute(text("""
                CREATE TABLE ethical_bias_profiles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                    primary_framework VARCHAR,
                    secondary_frameworks JSONB DEFAULT '[]'::jsonb,
                    reasoning_patterns JSONB DEFAULT '{}'::jsonb,
                    summary TEXT,
                    recommendations JSONB DEFAULT '[]'::jsonb,
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_justification_id INTEGER
                )
            """))
            # Create index on user_id
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_ethical_bias_profiles_user_id 
                ON ethical_bias_profiles(user_id)
            """))
            print("✓ Created ethical_bias_profiles table")
        else:
            print("✓ ethical_bias_profiles table already exists")
        
        # 2. Remove ethical_bias_summary column from quiz_attempts if it exists
        check_column = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'quiz_attempts' 
            AND column_name = 'ethical_bias_summary'
        """)
        result = conn.execute(check_column)
        column_exists = result.fetchone() is not None
        
        if column_exists:
            print("Removing ethical_bias_summary column from quiz_attempts...")
            conn.execute(text("""
                ALTER TABLE quiz_attempts 
                DROP COLUMN IF EXISTS ethical_bias_summary
            """))
            print("✓ Removed ethical_bias_summary column")
        else:
            print("✓ ethical_bias_summary column does not exist (already removed)")
        
        print("\nMigration completed successfully!")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"Error during migration: {e}")
        raise

