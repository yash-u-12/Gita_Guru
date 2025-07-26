import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_utils import db_manager

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def populate_database():
    """Populate database with chapters and slokas from JSON files"""
    
    print("Starting database population...")
    
    # JSON files to process
    json_files = [
        'chapter12.json',
        'chapter15.json', 
        'chapter16.json'
    ]
    
    chapters_created = []
    slokas_created = []
    
    for json_file in json_files:
        print(f"\nProcessing {json_file}...")
        
        # Load JSON data
        data = load_json_data(json_file)
        if not data:
            continue
            
        # Get first sloka to extract chapter info
        if not data:
            print(f"No data found in {json_file}")
            continue
            
        first_sloka = data[0]
        chapter_number = first_sloka['chapter']
        chapter_name = first_sloka.get('chapter_name', f'Chapter {chapter_number}')
        
        print(f"Chapter {chapter_number}: {chapter_name}")
        
        # Check if chapter already exists
        existing_chapter = db_manager.get_chapter_by_number(chapter_number)
        if existing_chapter:
            print(f"  Chapter {chapter_number} already exists, skipping...")
            chapter_id = existing_chapter['id']
        else:
            # Create chapter
            chapter = db_manager.create_chapter(chapter_number, chapter_name)
            if chapter:
                chapter_id = chapter['id']
                chapters_created.append(chapter)
                print(f"  ✅ Created chapter: {chapter_name}")
            else:
                print(f"  ❌ Failed to create chapter {chapter_number}")
                continue
        
        # Process slokas
        for sloka_data in data:
            if 'sloka_number' not in sloka_data:
                print(f"    Skipping entry without sloka_number: {sloka_data.get('sloka_title', 'Unknown')}")
                continue
            sloka_number = int(sloka_data['sloka_number'])
            
            # Check if sloka already exists
            existing_sloka = db_manager.get_sloka_by_chapter_and_number(chapter_id, sloka_number)
            if existing_sloka:
                print(f"    Sloka {sloka_number} already exists, skipping...")
                continue
            
            # Create sloka (without audio URL for now)
            sloka = db_manager.create_sloka(
                chapter_id=chapter_id,
                sloka_number=sloka_number,
                sloka_text_telugu=sloka_data['sloka_text'],
                meaning_telugu=sloka_data['telugu_meaning'],
                meaning_english=sloka_data['english_meaning']
            )
            
            if sloka:
                slokas_created.append(sloka)
                print(f"    ✅ Created sloka {sloka_number}")
            else:
                print(f"    ❌ Failed to create sloka {sloka_number}")
    
    # Print summary
    print(f"\n{'='*50}")
    print("DATABASE POPULATION SUMMARY")
    print(f"{'='*50}")
    print(f"Chapters created: {len(chapters_created)}")
    print(f"Slokas created: {len(slokas_created)}")
    
    if chapters_created:
        print(f"\nChapters created:")
        for chapter in chapters_created:
            print(f"  Chapter {chapter['chapter_number']}: {chapter['chapter_name']}")
    
    print(f"\nDatabase population completed!")
    
    return chapters_created, slokas_created

if __name__ == "__main__":
    populate_database() 