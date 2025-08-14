import streamlit as st
import sys
import os
import uuid
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import wave, contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_utils import db_manager

# Page config
st.set_page_config(
    page_title="Gita Guru - Divine Learning", 
    page_icon="🕉️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple and clean CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .header-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        color: white;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .welcome-text {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .content-section {
        background: transparent;
        padding: 1rem 0;
        margin: 1rem 0;
    }
    
    .sloka-display {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .meaning-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .meaning-title {
        font-weight: 600;
        color: white;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .meaning-icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    .sloka-text {
        color: white;
        font-size: 1.2rem;
        line-height: 1.8;
    }
    
    .meaning-text {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Auth guard
if "user" not in st.session_state:
    st.error("You must be signed in to view this page.")
    st.stop()

user = st.session_state["user"]

# Header section
st.markdown(f"""
<div class="header-section">
    <div class="main-title">🕉️ Gita Guru</div>
    <div class="welcome-text">Welcome back, <strong>{user.get('name','User')}</strong>! 🙏</div>
    <div style="opacity: 0.8;">Select a chapter and sloka to begin your spiritual journey</div>
</div>
""", unsafe_allow_html=True)

# Get chapters
chapters = db_manager.get_all_chapters()
if not chapters:
    st.error("No chapters found. Please check your database connection.")
    st.stop()

# Create chapter options for dropdown
chapter_options = ["Select a Chapter"] + [f"Chapter {ch['chapter_number']}: {ch['chapter_name']}" for ch in chapters]
chapter_dict = {f"Chapter {ch['chapter_number']}: {ch['chapter_name']}": ch for ch in chapters}

# Chapter selection dropdown
st.markdown("### 📚 Select Chapter")
selected_chapter_option = st.selectbox(
    "Choose a chapter to explore:",
    options=chapter_options,
    key="chapter_selector"
)

# If a chapter is selected, show sloka dropdown
if selected_chapter_option != "Select a Chapter":
    selected_chapter = chapter_dict[selected_chapter_option]
    slokas = db_manager.get_slokas_by_chapter(selected_chapter["id"])
    
    if not slokas:
        st.info("No slokas found for this chapter.")
    else:
        # Create sloka options for dropdown
        sloka_options = ["Select a Sloka"] + [f"Sloka {sl['sloka_number']}" for sl in slokas]
        sloka_dict = {f"Sloka {sl['sloka_number']}": sl for sl in slokas}
        
        st.markdown("### 🎯 Select Sloka")
        selected_sloka_option = st.selectbox(
            "Choose a sloka to read:",
            options=sloka_options,
            key="sloka_selector"
        )
        
        # If a sloka is selected, display it
        if selected_sloka_option != "Select a Sloka":
            selected_sloka = sloka_dict[selected_sloka_option]
            
            # Display sloka content
            st.markdown("""
            <div class="content-section">
            """, unsafe_allow_html=True)
            
            st.markdown(f"### 📖 Sloka {selected_sloka['sloka_number']} - Chapter {selected_chapter['chapter_number']}: {selected_chapter['chapter_name']}")
            
            # Sloka text
            st.markdown("""
            <div class="sloka-display">
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="sloka-text">
                {selected_sloka.get('sloka_text_telugu', 'Text not available')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Meanings
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="meaning-section">
                    <div class="meaning-title">
                        <span class="meaning-icon">📖</span>
                        Telugu Meaning
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="meaning-text">
                    {selected_sloka.get('meaning_telugu', 'Meaning not available')}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="meaning-section">
                    <div class="meaning-title">
                        <span class="meaning-icon">🌍</span>
                        English Meaning
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="meaning-text">
                    {selected_sloka.get('meaning_english', 'Meaning not available')}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Audio section
            st.markdown("### 🎵 Reference Audio")
            ref_url = selected_sloka.get("reference_audio_url")
            if ref_url:
                st.audio(ref_url, format="audio/mp3")
            else:
                st.info("No reference audio available for this sloka.")
            
            # Submission section
            st.markdown("### 🎤 Share Your Learning")
            st.info("Record your recitation and explanation. Looks and works like WhatsApp.")

            with st.expander("🎙️ Record Your Audio", expanded=True):
                col1, col2 = st.columns(2)

                # Restore previous recordings if any
                rec_key = f"rec_audio_{selected_sloka['id']}"
                exp_key = f"exp_audio_{selected_sloka['id']}"
                rec_bytes = st.session_state.get(rec_key)
                exp_bytes = st.session_state.get(exp_key)

                def duration_mm_ss(audio_bytes: bytes) -> str:
                    try:
                        with contextlib.closing(wave.open(BytesIO(audio_bytes), 'rb')) as wf:
                            frames = wf.getnframes()
                            rate = wf.getframerate()
                            secs = int(frames / float(rate))
                            return f"{secs // 60:02d}:{secs % 60:02d}"
                    except Exception:
                        return "00:00"

                # Add/reset counters to force widget to reset on delete
                rec_rev_key = f"rec_rev_{selected_sloka['id']}"
                exp_rev_key = f"exp_rev_{selected_sloka['id']}"
                if rec_rev_key not in st.session_state:
                    st.session_state[rec_rev_key] = 0
                if exp_rev_key not in st.session_state:
                    st.session_state[exp_rev_key] = 0

                with col1:
                    st.markdown("**🎤 Recitation Recording**")
                    st.markdown("""
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin: 0.5rem 0; text-align: center; border: 2px solid rgba(255,255,255,0.2);">
                        <div style="color: white; font-weight: 600; margin-bottom: 1rem; font-size: 16px;">📖 Record Sloka Recitation</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 1.5rem;">Tap mic to start/stop recording</div>
                    </div>
                    """, unsafe_allow_html=True)

                    new_rec = audio_recorder(
                        text="🎙️",
                        recording_color="#dc3545",
                        neutral_color="#25D366",
                        icon_name="microphone",
                        icon_size="3x",
                        key=f"rec_audio_widget_{selected_sloka['id']}_{st.session_state[rec_rev_key]}",
                    )
                    if new_rec:  # capture after stop
                        st.session_state[rec_key] = new_rec
                        rec_bytes = new_rec

                    if rec_bytes:
                        st.markdown("✅ Recitation recorded")
                        st.audio(rec_bytes, format="audio/wav")
                        st.caption(f"⏱️ Duration: {duration_mm_ss(rec_bytes)}")
                        if st.button("🗑️ Delete Recitation", key=f"del_rec_{selected_sloka['id']}"):
                            st.session_state.pop(rec_key, None)
                            st.session_state[rec_rev_key] += 1  # force new widget key
                            st.rerun()
                    rec_file = st.file_uploader(
                        "Or upload recitation file", type=["mp3", "wav"], key=f"rec_file_{selected_sloka['id']}"
                    )

                with col2:
                    st.markdown("**💭 Explanation Recording**")
                    st.markdown("""
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin: 0.5rem 0; text-align: center; border: 2px solid rgba(255,255,255,0.2);">
                        <div style="color: white; font-weight: 600; margin-bottom: 1rem; font-size: 16px;">💭 Record Explanation</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 1.5rem;">Tap mic to start/stop recording</div>
                    </div>
                    """, unsafe_allow_html=True)

                    new_exp = audio_recorder(
                        text="🎙️",
                        recording_color="#dc3545",
                        neutral_color="#25D366",
                        icon_name="microphone",
                        icon_size="3x",
                        key=f"exp_audio_widget_{selected_sloka['id']}_{st.session_state[exp_rev_key]}",
                    )
                    if new_exp:
                        st.session_state[exp_key] = new_exp
                        exp_bytes = new_exp

                    if exp_bytes:
                        st.markdown("✅ Explanation recorded")
                        st.audio(exp_bytes, format="audio/wav")
                        st.caption(f"⏱️ Duration: {duration_mm_ss(exp_bytes)}")
                        if st.button("🗑️ Delete Explanation", key=f"del_exp_{selected_sloka['id']}"):
                            st.session_state.pop(exp_key, None)
                            st.session_state[exp_rev_key] += 1  # force new widget key
                            st.rerun()
                    exp_file = st.file_uploader(
                        "Or upload explanation file", type=["mp3", "wav"], key=f"exp_file_{selected_sloka['id']}"
                    )

            # Submit without a form (works better with recorder widgets)
            submit_btn = st.button("🚀 Submit Learning", use_container_width=True)
            if submit_btn:
                if not (st.session_state.get(rec_key) or st.session_state.get(exp_key) or rec_file or exp_file):
                    st.markdown('<div class="error-message">Please record or upload at least one audio file.</div>', unsafe_allow_html=True)
                else:
                    try:
                        bucket = "audio"
                        rec_url = None
                        exp_url = None

                        if st.session_state.get(rec_key):
                            rec_name = f"user_submissions/{user['id']}/rec_{selected_sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}.wav"
                            db_manager.supabase.storage.from_(bucket).upload(rec_name, st.session_state[rec_key])
                            rec_url = db_manager.supabase.storage.from_(bucket).get_public_url(rec_name)
                        elif rec_file:
                            rec_name = f"user_submissions/{user['id']}/rec_{selected_sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}{os.path.splitext(rec_file.name)[1]}"
                            db_manager.supabase.storage.from_(bucket).upload(rec_name, rec_file.read())
                            rec_url = db_manager.supabase.storage.from_(bucket).get_public_url(rec_name)

                        if st.session_state.get(exp_key):
                            exp_name = f"user_submissions/{user['id']}/exp_{selected_sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}.wav"
                            db_manager.supabase.storage.from_(bucket).upload(exp_name, st.session_state[exp_key])
                            exp_url = db_manager.supabase.storage.from_(bucket).get_public_url(exp_name)
                        elif exp_file:
                            exp_name = f"user_submissions/{user['id']}/exp_{selected_sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}{os.path.splitext(exp_file.name)[1]}"
                            db_manager.supabase.storage.from_(bucket).upload(exp_name, exp_file.read())
                            exp_url = db_manager.supabase.storage.from_(bucket).get_public_url(exp_name)

                        db_manager.create_user_submission(
                            user_id=user['id'],
                            sloka_id=selected_sloka['id'],
                            recitation_audio_url=rec_url,
                            explanation_audio_url=exp_url
                        )
                        st.markdown('<div class="success-message">✅ Your submission has been saved successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-message">❌ Submission failed: {str(e)}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem 0; opacity: 0.8;">
    <p>🕉️ May the divine wisdom guide your path</p>
    <p><small>Gita Guru - Divine Learning Platform</small></p>
</div>
""", unsafe_allow_html=True)


