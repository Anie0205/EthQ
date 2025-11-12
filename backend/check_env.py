"""
Environment variable validation script.
Run this to check if all required environment variables are set.
"""
import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = {
    "SECRET_KEY": "JWT token signing key",
    "DATABASE_URL": "PostgreSQL database connection string",
    "GEMINI_API_KEY": "Google Gemini API key for quiz generation",
}

OPTIONAL_VARS = {
    "PORT": "Server port (defaults to 8000)",
    "ALLOWED_ORIGINS": "CORS allowed origins (comma-separated)",
    "ENVIRONMENT": "Environment name (development/production)",
}

def check_environment():
    """Check all environment variables and report status."""
    print("=" * 60)
    print("Environment Variable Check")
    print("=" * 60)
    
    missing = []
    present = []
    
    for var, description in REQUIRED_VARS.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "SECRET" in var or "PASSWORD" in var:
                masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                print(f"✓ {var:20} = {masked:20} ({description})")
            else:
                print(f"✓ {var:20} = {value[:50]:50} ({description})")
            present.append(var)
        else:
            print(f"✗ {var:20} = MISSING            ({description})")
            missing.append(var)
    
    print("\nOptional Variables:")
    for var, description in OPTIONAL_VARS.items():
        value = os.getenv(var)
        if value:
            print(f"  {var:20} = {value[:50]:50} ({description})")
        else:
            print(f"  {var:20} = (not set)          ({description})")
    
    print("\n" + "=" * 60)
    if missing:
        print(f"❌ {len(missing)} required variable(s) missing!")
        print("Please set the following environment variables:")
        for var in missing:
            print(f"  - {var}")
        return False
    else:
        print(f"✅ All required environment variables are set!")
        return True

if __name__ == "__main__":
    success = check_environment()
    exit(0 if success else 1)

