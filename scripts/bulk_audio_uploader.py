import os
import glob
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, AUDIO_STORAGE_PATH

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('ascii', errors='ignore'))

def upload_audio_files():
    """Upload all audio files from slokas folder to Supabase Storage"""
    
    safe_print(f"Using Supabase URL: {SUPABASE_URL}")
    safe_print(f"Storage path: {AUDIO_STORAGE_PATH}")
    
    # Initialize Supabase client
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        safe_print("✅ Supabase client initialized successfully")
    except Exception as e:
        safe_print(f"❌ Failed to initialize Supabase client: {str(e)}")
        return [], []
    
    base_path = "slokas"
    upload_results = []
    failed_uploads = []
    
    safe_print("Starting bulk audio upload to Supabase Storage...")
    
    for chapter_folder in sorted(os.listdir(base_path)):
        chapter_path = os.path.join(base_path, chapter_folder)
        
        if not os.path.isdir(chapter_path) or not chapter_folder.isdigit():
            continue
            
        chapter_number = int(chapter_folder)
        safe_print(f"\nProcessing Chapter {chapter_number}...")
        
        mp3_files = glob.glob(os.path.join(chapter_path, "*.mp3"))
        
        for mp3_file in sorted(mp3_files):
            filename = os.path.basename(mp3_file)
            sloka_number = filename.replace('.mp3', '')
            
            if 'pushpika' in sloka_number.lower():
                safe_print(f"  Skipping special file: {filename}")
                continue
                
            storage_path = f"{AUDIO_STORAGE_PATH}/{chapter_number}/{sloka_number}.mp3"
            
            try:
                safe_print(f"  Uploading: {filename} -> {storage_path}")
                
                with open(mp3_file, 'rb') as file:
                    result = supabase.storage.from_('public').upload(
                        path=storage_path,
                        file=file,
                        file_options={"content-type": "audio/mpeg", "upsert": "true"}
                    )
                
                safe_print(f"    Upload result: {result}")
                
                public_url = supabase.storage.from_('public').get_public_url(storage_path)
                
                upload_results.append({
                    'chapter': chapter_number,
                    'sloka': sloka_number,
                    'filename': filename,
                    'storage_path': storage_path,
                    'public_url': public_url,
                    'status': 'success'
                })
                
                safe_print(f"    ✅ Success: {public_url}")
                
            except Exception as e:
                error_msg = f"Failed to upload {filename}: {str(e)}"
                safe_print(f"    ❌ {error_msg}")
                failed_uploads.append({
                    'chapter': chapter_number,
                    'sloka': sloka_number,
                    'filename': filename,
                    'error': str(e)
                })
    
    safe_print(f"\n{'='*50}")
    safe_print("UPLOAD SUMMARY")
    safe_print(f"{'='*50}")
    safe_print(f"Total successful uploads: {len(upload_results)}")
    safe_print(f"Total failed uploads: {len(failed_uploads)}")
    
    if upload_results:
        safe_print(f"\nSuccessful uploads:")
        for result in upload_results:
            safe_print(f"  Chapter {result['chapter']}, Sloka {result['sloka']}: {result['public_url']}")
    
    if failed_uploads:
        safe_print(f"\nFailed uploads:")
        for failure in failed_uploads:
            safe_print(f"  Chapter {failure['chapter']}, Sloka {failure['sloka']}: {failure['error']}")
    
    try:
        with open('upload_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'successful_uploads': upload_results,
                'failed_uploads': failed_uploads
            }, f, indent=2, ensure_ascii=False)
        
        safe_print(f"\nResults saved to upload_results.json")
    except Exception as e:
        safe_print(f"❌ Failed to save upload_results.json: {str(e)}")
    
    return upload_results, failed_uploads

if __name__ == "__main__":
    upload_audio_files()
