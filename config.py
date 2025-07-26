
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = "https://jutfhqtwfdmgedmdmizz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDU0OTUsImV4cCI6MjA2OTA4MTQ5NX0.YKGcX4OvtQNJiNndKvC9mlX8gOC2xHpOuM2xnOrjI44"

# Storage Configuration
AUDIO_STORAGE_PATH = "gita-guru/audio"
USER_SUBMISSIONS_PATH = "gita-guru/submissions"

# Database Configuration
DATABASE_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD', 'GitaGuru21206')}@db.{SUPABASE_URL.split('//')[1].split('.')[0]}.supabase.co:5432/postgres"

# Admin Configuration
ADMIN_PASSWORD = "admin123"

# Chapter Configuration
CHAPTERS_DATA = {
    12: "chapter12.json",
    15: "chapter15.json", 
    16: "chapter16.json"
}
