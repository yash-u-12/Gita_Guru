import os
import glob
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, AUDIO_STORAGE_PATH

def upload_audio_files():
    """Upload all audio files from slokas folder to Supabase Storage"""
    
    print(f"Using Supabase URL: {SUPABASE_URL}")
    print(f"Storage path: {AUDIO_STORAGE_PATH}")
    
    # Initialize Supabase client
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {str(e)}")
        return [], []
    
    # Base path for audio files
    base_path = "slokas"
    
    # Track upload results
    upload_results = []
    failed_uploads = []
    
    print("Starting bulk audio upload to Supabase Storage...")
    
    # Scan through all chapter folders
    for chapter_folder in sorted(os.listdir(base_path)):
        chapter_path = os.path.join(base_path, chapter_folder)
        
        # Skip if not a directory or doesn't contain numbers (chapter numbers)
        if not os.path.isdir(chapter_path) or not chapter_folder.isdigit():
            continue
            
        chapter_number = int(chapter_folder)
        print(f"\nProcessing Chapter {chapter_number}...")
        
        # Find all MP3 files in the chapter folder
        mp3_files = glob.glob(os.path.join(chapter_path, "*.mp3"))
        
        for mp3_file in sorted(mp3_files):
            filename = os.path.basename(mp3_file)
            
            # Extract sloka number from filename (remove .mp3 extension)
            sloka_number = filename.replace('.mp3', '')
            
            # Skip special files like pushpika
            if 'pushpika' in sloka_number.lower():
                print(f"  Skipping special file: {filename}")
                continue
                
            # Create storage path
            storage_path = f"{AUDIO_STORAGE_PATH}/{chapter_number}/{sloka_number}.mp3"
            
            try:
                print(f"  Uploading: {filename} -> {storage_path}")
                
                # Upload file to Supabase Storage
                with open(mp3_file, 'rb') as file:
                    result = supabase.storage.from_('public').upload(
                        path=storage_path,
                        file=file,
                        file_options={"content-type": "audio/mpeg", "upsert": "true"}
                    )
                
                print(f"    Upload result: {result}")
                
                # Get public URL
                public_url = supabase.storage.from_('public').get_public_url(storage_path)
                
                upload_results.append({
                    'chapter': chapter_number,
                    'sloka': sloka_number,
                    'filename': filename,
                    'storage_path': storage_path,
                    'public_url': public_url,
                    'status': 'success'
                })
                
                print(f"    ✅ Success: {public_url}")
                
            except Exception as e:
                error_msg = f"Failed to upload {filename}: {str(e)}"
                print(f"    ❌ {error_msg}")
                failed_uploads.append({
                    'chapter': chapter_number,
                    'sloka': sloka_number,
                    'filename': filename,
                    'error': str(e)
                })
    
    # Print summary
    print(f"\n{'='*50}")
    print("UPLOAD SUMMARY")
    print(f"{'='*50}")
    print(f"Total successful uploads: {len(upload_results)}")
    print(f"Total failed uploads: {len(failed_uploads)}")
    
    if upload_results:
        print(f"\nSuccessful uploads:")
        for result in upload_results:
            print(f"  Chapter {result['chapter']}, Sloka {result['sloka']}: {result['public_url']}")
    
    if failed_uploads:
        print(f"\nFailed uploads:")
        for failure in failed_uploads:
            print(f"  Chapter {failure['chapter']}, Sloka {failure['sloka']}: {failure['error']}")
    
    # Save results to file for reference
    try:
        with open('upload_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'successful_uploads': upload_results,
                'failed_uploads': failed_uploads
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to upload_results.json")
    except Exception as e:
        print(f"❌ Failed to save upload_results.json: {str(e)}")
    
    return upload_results, failed_uploads

if __name__ == "__main__":
    upload_audio_files() 