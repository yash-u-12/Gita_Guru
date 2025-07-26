#!/usr/bin/env python3
"""
Gita Guru - Complete Setup Script
This script runs all the necessary steps to set up the Gita Guru platform.
"""

import os
import sys
import subprocess
import time

def print_step(step_number, title):
    """Print a formatted step header"""
    print(f"\n{'='*60}")
    print(f"STEP {step_number}: {title}")
    print(f"{'='*60}")

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running {script_path}: {e}")
        return False
    return True

def main():
    print("🕉️ GITA GURU - COMPLETE SETUP")
    print("This script will set up the entire Gita Guru platform.")
    print("\nPrerequisites:")
    print("- Supabase project configured")
    print("- JSON files for chapters available")
    print("- Audio files in slokas/ folder")
    
    # Ask for confirmation
    response = input("\nDo you want to continue? (y/N): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return
    
    # Step 1: Install dependencies
    print_step(1, "INSTALLING DEPENDENCIES")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return
    
    # Step 2: Create database schema
    print_step(2, "CREATING DATABASE SCHEMA")
    print("Please run the SQL schema in your Supabase SQL editor:")
    print("File: database/schema.sql")
    input("Press Enter after running the schema...")
    
    # Step 3: Populate database with JSON data
    print_step(3, "POPULATING DATABASE WITH JSON DATA")
    if not run_script("scripts/db_populator.py", "Database population"):
        print("❌ Database population failed. Please check the errors above.")
        return
    
    # Step 4: Upload audio files to Supabase Storage
    print_step(4, "UPLOADING AUDIO FILES TO SUPABASE STORAGE")
    if not run_script("scripts/bulk_audio_uploader.py", "Audio file upload"):
        print("❌ Audio upload failed. Please check the errors above.")
        return
    
    # Step 5: Update database with audio URLs
    print_step(5, "UPDATING DATABASE WITH AUDIO URLS")
    if not run_script("scripts/db_audio_url_updater.py", "Audio URL updates"):
        print("❌ Audio URL updates failed. Please check the errors above.")
        return
    
    # Step 6: Final verification
    print_step(6, "FINAL VERIFICATION")
    print("✅ Setup completed successfully!")
    
    print("\n🎉 GITA GURU PLATFORM IS READY!")
    print("\nNext steps:")
    print("1. Run the user portal: streamlit run streamlit_app/user_portal.py")
    print("2. Run the admin dashboard: streamlit run streamlit_app/admin_dashboard.py")
    print("\nUser Portal Features:")
    print("- Browse chapters and slokas")
    print("- Listen to reference audio")
    print("- Upload recitation and explanation audios")
    print("- Track submission status")
    print("\nAdmin Dashboard Features:")
    print("- Review user submissions")
    print("- Approve/reject submissions")
    print("- View statistics")
    print("- Add admin notes")
    
    print(f"\nAdmin password: admin123")
    print("\nHappy learning! 🕉️")

if __name__ == "__main__":
    main() 