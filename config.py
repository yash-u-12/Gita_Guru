import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = "https://jutfhqtwfdmgedmdmizz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDU0OTUsImV4cCI6MjA2OTA4MTQ5NX0.YKGcX4OvtQNJiNndKvC9mlX8gOC2xHpOuM2xnOrjI44"

# Database Configuration
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")

# Storage Paths
AUDIO_STORAGE_PATH = "public/slokas/audio"
USER_SUBMISSIONS_PATH = "public/user_submissions" 