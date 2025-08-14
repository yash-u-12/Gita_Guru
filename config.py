import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration
# You need to set these values in your .env file or environment variables
SUPABASE_URL = "enter the supabase url"
SUPABASE_KEY = "Enter your supabase key hear"
AUDIO_STORAGE_PATH = r"gita\Gita_Guru\sloka"
SUPABASE_SERVICE_ROLE_KEY = "enter your supabase service role key hear" 

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
