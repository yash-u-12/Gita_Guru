import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration
# You need to set these values in your .env file or environment variables
SUPABASE_URL = "https://jutfhqtwfdmgedmdmizz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDU0OTUsImV4cCI6MjA2OTA4MTQ5NX0.YKGcX4OvtQNJiNndKvC9mlX8gOC2xHpOuM2xnOrjI44"
AUDIO_STORAGE_PATH = r"C:\Users\varshith\OneDrive\Desktop\gita\Gita_Guru\slokas"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MzUwNTQ5NSwiZXhwIjoyMDY5MDgxNDk1fQ.8O8mMdzVFXtbo--UlfhRjGDuXNSb93hw0RCpg-rfL2w" 

# Validate that required environment variables are set
if not SUPABASE_URL:
    raise ValueError("""
SUPABASE_URL environment variable is required. 

Please create a .env file in the project root with the following content:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

You can find these values in your Supabase dashboard under Settings > API.
""")
if not SUPABASE_KEY:
    raise ValueError("""
SUPABASE_KEY environment variable is required. 

Please create a .env file in the project root with the following content:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

You can find these values in your Supabase dashboard under Settings > API.
""")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("""
SUPABASE_SERVICE_ROLE_KEY environment variable is required. 

Please create a .env file in the project root with the following content:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

You can find these values in your Supabase dashboard under Settings > API.
""")
