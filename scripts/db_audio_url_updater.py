import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_utils import db_manager
from config import AUDIO_STORAGE_PATH

def update_audio_urls():
    """Update sloka records with uploaded audio URLs"""
    
    print("Starting audio URL updates...")
    
    # Load upload results
    try:
        with open('upload_results.json', 'r', encoding='utf-8') as f:
            upload_data = json.load(f)
    except FileNotFoundError:
        print("upload_results.json not found. Please run bulk_audio_uploader.py first.")
        return
    
    successful_uploads = upload_data.get('successful_uploads', [])
    
    if not successful_uploads:
        print("No successful uploads found.")
        return
    
    updated_count = 0
    failed_updates = []
    
    for upload in successful_uploads:
        chapter_number = upload['chapter']
        sloka_number = upload['sloka']
        public_url = upload['public_url']
        
        print(f"Updating Chapter {chapter_number}, Sloka {sloka_number}...")
        
        # Get chapter
        chapter = db_manager.get_chapter_by_number(chapter_number)
        if not chapter:
            print(f"  ❌ Chapter {chapter_number} not found in database")
            failed_updates.append({
                'chapter': chapter_number,
                'sloka': sloka_number,
                'error': 'Chapter not found'
            })
            continue
        
        # Get sloka
        sloka = db_manager.get_sloka_by_chapter_and_number(chapter['id'], sloka_number)
        if not sloka:
            print(f"  ❌ Sloka {sloka_number} not found in database")
            failed_updates.append({
                'chapter': chapter_number,
                'sloka': sloka_number,
                'error': 'Sloka not found'
            })
            continue
        
        # Update audio URL
        updated_sloka = db_manager.update_sloka_audio_url(sloka['id'], public_url)
        if updated_sloka:
            print(f"  ✅ Updated audio URL: {public_url}")
            updated_count += 1
        else:
            print(f"  ❌ Failed to update audio URL")
            failed_updates.append({
                'chapter': chapter_number,
                'sloka': sloka_number,
                'error': 'Database update failed'
            })
    
    # Print summary
    print(f"\n{'='*50}")
    print("AUDIO URL UPDATE SUMMARY")
    print(f"{'='*50}")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed updates: {len(failed_updates)}")
    
    if failed_updates:
        print(f"\nFailed updates:")
        for failure in failed_updates:
            print(f"  Chapter {failure['chapter']}, Sloka {failure['sloka']}: {failure['error']}")
    
    print(f"\nAudio URL updates completed!")
    
    return updated_count, failed_updates

if __name__ == "__main__":
    update_audio_urls() 