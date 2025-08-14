import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_json_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def populate_from_json_file(filepath):
    print(f"\n Processing: {os.path.basename(filepath)}")
    slokas = load_json_data(filepath)

    if not slokas or not isinstance(slokas, list):
        print(f"  Skipping file {filepath}: No valid data")
        return

    # Extract chapter info from first sloka
    chapter_number = int(slokas[0].get("chapter", 0))
    chapter_name = slokas[0].get("chapter_name", f"Chapter {chapter_number}")

    # --- Upsert Chapter ---
    # Upsert the chapter first
    supabase.table("chapters").upsert(
    {
        "chapter_number": chapter_number,
        "chapter_name": chapter_name,
    },
    on_conflict=["chapter_number"]
    ).execute()

    # Fetch the chapter ID manually after upsert
    chapter_response = supabase.table("chapters").select("id").eq("chapter_number", chapter_number).single().execute()
    chapter_id = chapter_response.data["id"]
    print(f" Upserted Chapter {chapter_number} (ID: {chapter_id})")

    # --- Upsert Slokas ---
    sloka_count = 0
    for sloka in slokas:
        if "sloka_number" not in sloka:
            print(f" Skipping invalid entry (missing sloka_number): {sloka.get('sloka_title', 'Unknown')}")
            continue

        sloka_number = int(sloka["sloka_number"])
        sloka_text = sloka.get("sloka_text", "")
        telugu_meaning = sloka.get("telugu_meaning", "")
        english_meaning = sloka.get("english_meaning", "")
        reference_audio_url = sloka.get("reference_audio_url", "")

        supabase.table("slokas").upsert(
            {
                "chapter_id": chapter_id,
                "sloka_number": sloka_number,
                "sloka_text_telugu": sloka_text,
                "meaning_telugu": telugu_meaning,
                "meaning_english": english_meaning,
                "reference_audio_url": reference_audio_url,
            },
            on_conflict="chapter_id,sloka_number"
        ).execute()
        sloka_count += 1
        print(f"   -  Upserted Sloka {sloka_number}")

    print(f" Total Slokas Processed: {sloka_count}")

def populate_all_chapters():
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f" 'data/' folder not found.")
        return

    json_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

    if not json_files:
        print("  No JSON files found in the 'data/' folder.")
        return

    print(f" Found {len(json_files)} chapter file(s): {json_files}")
    for file_name in json_files:
        file_path = os.path.join(data_dir, file_name)
        populate_from_json_file(file_path)

    print("\n All chapters processed successfully.")

if __name__ == "__main__":
    populate_all_chapters()
