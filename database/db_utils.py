import json
import os
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

class DatabaseManager:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def create_chapter(self, chapter_number: int, chapter_name: str):
        """Create a new chapter"""
        try:
            data = {
                'chapter_number': chapter_number,
                'chapter_name': chapter_name
            }
            result = self.supabase.table('chapters').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating chapter {chapter_number}: {e}")
            return None
    
    def create_sloka(self, chapter_id: str, sloka_number: int, sloka_text_telugu: str, 
                     meaning_telugu: str, meaning_english: str, reference_audio_url: str = None):
        """Create a new sloka"""
        try:
            data = {
                'chapter_id': chapter_id,
                'sloka_number': sloka_number,
                'sloka_text_telugu': sloka_text_telugu,
                'meaning_telugu': meaning_telugu,
                'meaning_english': meaning_english,
                'reference_audio_url': reference_audio_url
            }
            result = self.supabase.table('slokas').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating sloka {sloka_number}: {e}")
            return None
    
    def get_chapter_by_number(self, chapter_number: int):
        """Get chapter by chapter number"""
        try:
            result = self.supabase.table('chapters').select('*').eq('chapter_number', chapter_number).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting chapter {chapter_number}: {e}")
            return None
    
    def get_sloka_by_chapter_and_number(self, chapter_id: str, sloka_number: int):
        """Get sloka by chapter_id and sloka_number"""
        try:
            result = self.supabase.table('slokas').select('*').eq('chapter_id', chapter_id).eq('sloka_number', sloka_number).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting sloka {sloka_number}: {e}")
            return None
    
    def update_sloka_audio_url(self, sloka_id: str, audio_url: str):
        """Update sloka reference audio URL"""
        try:
            result = self.supabase.table('slokas').update({'reference_audio_url': audio_url}).eq('id', sloka_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating sloka audio URL: {e}")
            return None
    
    def get_all_chapters(self):
        """Get all chapters ordered by chapter number"""
        try:
            result = self.supabase.table('chapters').select('*').order('chapter_number').execute()
            return result.data
        except Exception as e:
            print(f"Error getting chapters: {e}")
            return []
    
    def get_slokas_by_chapter(self, chapter_id: str):
        """Get all slokas for a chapter ordered by sloka number"""
        try:
            result = self.supabase.table('slokas').select('*').eq('chapter_id', chapter_id).order('sloka_number').execute()
            return result.data
        except Exception as e:
            print(f"Error getting slokas for chapter {chapter_id}: {e}")
            return []
    
    def create_user(self, name: str, email: str):
        """Create a new user"""
        try:
            data = {
                'name': name,
                'email': email
            }
            result = self.supabase.table('users').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email: str):
        """Get user by email"""
        try:
            result = self.supabase.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def create_user_submission(self, user_id: str, sloka_id: str, recitation_audio_url: str = None, explanation_audio_url: str = None):
        """Create a new user submission"""
        try:
            data = {
                'user_id': user_id,
                'sloka_id': sloka_id,
                'recitation_audio_url': recitation_audio_url,
                'explanation_audio_url': explanation_audio_url,
                'status': 'Submitted'
            }
            result = self.supabase.table('user_submissions').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user submission: {e}")
            return None
    
    def get_user_submissions(self, user_id: str = None, sloka_id: str = None, status: str = None):
        """Get user submissions with optional filters"""
        try:
            query = self.supabase.table('user_submissions').select('*, users(name, email), slokas(sloka_number, slokas_text_telugu)')
            
            if user_id:
                query = query.eq('user_id', user_id)
            if sloka_id:
                query = query.eq('sloka_id', sloka_id)
            if status:
                query = query.eq('status', status)
            
            result = query.order('created_at', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error getting user submissions: {e}")
            return []
    
    def update_submission_status(self, submission_id: str, status: str, admin_notes: str = None):
        """Update submission status"""
        try:
            data = {'status': status}
            if admin_notes:
                data['admin_notes'] = admin_notes
            
            result = self.supabase.table('user_submissions').update(data).eq('id', submission_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating submission status: {e}")
            return None

# Global database manager instance
db_manager = DatabaseManager() 