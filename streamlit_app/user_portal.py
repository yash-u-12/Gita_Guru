import streamlit as st
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_utils import db_manager
from config import SUPABASE_URL, SUPABASE_KEY, USER_SUBMISSIONS_PATH
from supabase import create_client

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Learn Bhagavad Gita",
    page_icon="🕉️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .sloka-text {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .meaning-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .upload-section {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🕉️ Gita Guru</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Learn Bhagavad Gita with Audio</h2>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Learn Slokas", "My Submissions", "About"]
    )
    
    if page == "Learn Slokas":
        show_learn_page()
    elif page == "My Submissions":
        show_submissions_page()
    elif page == "About":
        show_about_page()

def show_learn_page():
    st.header("📖 Learn Slokas")
    
    # Get all chapters
    chapters = db_manager.get_all_chapters()
    
    if not chapters:
        st.error("No chapters found in database. Please run the database population script first.")
        return
    
    # Chapter selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Chapter")
        selected_chapter = st.selectbox(
            "Choose a chapter:",
            chapters,
            format_func=lambda x: f"Chapter {x['chapter_number']}: {x['chapter_name']}"
        )
    
    if selected_chapter:
        # Get slokas for selected chapter
        slokas = db_manager.get_slokas_by_chapter(selected_chapter['id'])
        
        with col2:
            st.subheader("Select Sloka")
            if slokas:
                selected_sloka = st.selectbox(
                    "Choose a sloka:",
                    slokas,
                    format_func=lambda x: f"Sloka {x['sloka_number']}"
                )
                
                if selected_sloka:
                    display_sloka_details(selected_sloka, selected_chapter)
            else:
                st.warning("No slokas found for this chapter.")

def display_sloka_details(sloka, chapter):
    st.markdown("---")
    st.markdown(f"### Chapter {chapter['chapter_number']}: {chapter['chapter_name']} - Sloka {sloka['sloka_number']}")
    
    # Sloka text
    st.markdown('<div class="sloka-text">', unsafe_allow_html=True)
    st.markdown("**Sloka Text (Telugu):**")
    st.markdown(sloka['sloka_text_telugu'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Meanings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="meaning-box">', unsafe_allow_html=True)
        st.markdown("**Telugu Meaning:**")
        st.markdown(sloka['meaning_telugu'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="meaning-box">', unsafe_allow_html=True)
        st.markdown("**English Meaning:**")
        st.markdown(sloka['meaning_english'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reference audio
    if sloka['reference_audio_url']:
        st.markdown("### 🎵 Reference Audio")
        st.audio(sloka['reference_audio_url'])
    else:
        st.warning("Reference audio not available for this sloka.")
    
    # Upload section
    st.markdown("---")
    st.markdown("### 📤 Submit Your Recitation & Explanation")
    
    # User registration/login
    user = get_or_create_user()
    
    if user:
        upload_user_submissions(sloka, user)

def get_or_create_user():
    """Get or create user based on email"""
    st.markdown("#### User Information")
    
    with st.form("user_form"):
        name = st.text_input("Your Name", key="user_name")
        email = st.text_input("Your Email", key="user_email")
        submit_user = st.form_submit_button("Continue")
    
    if submit_user and name and email:
        # Check if user exists
        existing_user = db_manager.get_user_by_email(email)
        if existing_user:
            st.success(f"Welcome back, {existing_user['name']}!")
            return existing_user
        else:
            # Create new user
            new_user = db_manager.create_user(name, email)
            if new_user:
                st.success(f"Welcome, {new_user['name']}! Your account has been created.")
                return new_user
            else:
                st.error("Failed to create user account.")
                return None
    
    return None

def upload_user_submissions(sloka, user):
    """Handle user audio uploads"""
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    with st.form("upload_form"):
        st.markdown("**Upload your recitation and explanation audios:**")
        
        recitation_audio = st.file_uploader(
            "Recitation Audio (MP3)",
            type=['mp3'],
            key="recitation"
        )
        
        explanation_audio = st.file_uploader(
            "Explanation Audio (MP3)", 
            type=['mp3'],
            key="explanation"
        )
        
        submit_upload = st.form_submit_button("Submit Audio")
    
    if submit_upload:
        if not recitation_audio and not explanation_audio:
            st.error("Please upload at least one audio file.")
            return
        
        # Upload files to Supabase Storage
        recitation_url = None
        explanation_url = None
        
        try:
            if recitation_audio:
                recitation_url = upload_audio_file(
                    recitation_audio, 
                    user['id'], 
                    sloka['id'], 
                    'recitation'
                )
            
            if explanation_audio:
                explanation_url = upload_audio_file(
                    explanation_audio, 
                    user['id'], 
                    sloka['id'], 
                    'explanation'
                )
            
            # Create submission record
            submission = db_manager.create_user_submission(
                user_id=user['id'],
                sloka_id=sloka['id'],
                recitation_audio_url=recitation_url,
                explanation_audio_url=explanation_url
            )
            
            if submission:
                st.success("✅ Your submission has been uploaded successfully!")
                st.info("Your submission will be reviewed by our team. You can check the status in 'My Submissions'.")
            else:
                st.error("Failed to create submission record.")
                
        except Exception as e:
            st.error(f"Error uploading files: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def upload_audio_file(audio_file, user_id, sloka_id, audio_type):
    """Upload audio file to Supabase Storage"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Create storage path
        storage_path = f"{USER_SUBMISSIONS_PATH}/{user_id}/{sloka_id}/{audio_type}.mp3"
        
        # Upload to Supabase Storage
        with open(tmp_file_path, 'rb') as file:
            supabase.storage.from_('public').upload(
                path=storage_path,
                file=file,
                file_options={"content-type": "audio/mpeg"}
            )
        
        # Get public URL
        public_url = supabase.storage.from_('public').get_public_url(storage_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return public_url
        
    except Exception as e:
        st.error(f"Error uploading {audio_type} audio: {str(e)}")
        return None

def show_submissions_page():
    st.header("📋 My Submissions")
    
    # Get user by email
    st.markdown("#### Enter your email to view submissions:")
    email = st.text_input("Email", key="submissions_email")
    
    if email:
        user = db_manager.get_user_by_email(email)
        if user:
            st.success(f"Showing submissions for {user['name']}")
            
            # Get user submissions
            submissions = db_manager.get_user_submissions(user_id=user['id'])
            
            if submissions:
                for submission in submissions:
                    with st.expander(f"Submission {submission['id'][:8]} - {submission['created_at'][:10]}"):
                        st.markdown(f"**Status:** {submission['status']}")
                        
                        if submission['recitation_audio_url']:
                            st.markdown("**Recitation Audio:**")
                            st.audio(submission['recitation_audio_url'])
                        
                        if submission['explanation_audio_url']:
                            st.markdown("**Explanation Audio:**")
                            st.audio(submission['explanation_audio_url'])
                        
                        if submission['admin_notes']:
                            st.markdown(f"**Admin Notes:** {submission['admin_notes']}")
            else:
                st.info("No submissions found for this user.")
        else:
            st.error("User not found. Please check your email address.")

def show_about_page():
    st.header("ℹ️ About Gita Guru")
    
    st.markdown("""
    ### Welcome to Gita Guru
    
    Gita Guru is a comprehensive learning platform for studying the Bhagavad Gita. 
    Our platform provides:
    
    - **Complete Sloka Text** in Telugu
    - **Detailed Meanings** in both Telugu and English
    - **Reference Audio** for proper pronunciation
    - **Interactive Learning** through audio submissions
    
    ### How to Use
    
    1. **Browse Chapters**: Select any chapter from the sidebar
    2. **Choose Slokas**: Pick specific slokas to study
    3. **Listen & Learn**: Play reference audio and read meanings
    4. **Practice**: Upload your own recitation and explanation
    5. **Track Progress**: Monitor your submissions and feedback
    
    ### Features
    
    - 📖 **Complete Text**: All slokas with authentic Telugu text
    - 🎵 **Audio Learning**: Reference audio for proper pronunciation
    - 📝 **Dual Meanings**: Both Telugu and English explanations
    - 📤 **Interactive**: Submit your own recitations for review
    - 📊 **Progress Tracking**: Monitor your learning journey
    
    ### Contact
    
    For support or questions, please contact our team.
    """)

if __name__ == "__main__":
    main() 