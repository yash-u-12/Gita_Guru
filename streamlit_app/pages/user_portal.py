import streamlit as st
import sys
import os
import uuid
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_utils import db_manager

# Page config + styles (keeps your app.py styling idea but minimal for clarity)
st.set_page_config(page_title="Gita Guru - User Portal", page_icon="📜", layout="wide")

st.markdown("""
<style>
    .sloka-box { background:#fff; padding:16px; margin-bottom:16px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.06); }
    .submission-box { background:#f7f7f7; padding:12px; border-radius:8px; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

# Auth guard
if "user" not in st.session_state:
    st.error("You must be signed in to view this page.")
    st.stop()

user = st.session_state["user"]
st.title("🕉️ Gita Guru")
st.write(f"Hello, **{user.get('name','User')}** 👋")
st.write("---")

# Chapters
chapters = db_manager.get_all_chapters()
if not chapters:
    st.warning("No chapters found.")
    st.stop()

chapter_map = {f"{c['chapter_number']}. {c['chapter_name']}": c for c in chapters}
choice = st.selectbox("Choose chapter", list(chapter_map.keys()))
chapter = chapter_map[choice]
chapter_id = chapter["id"]

slokas = db_manager.get_slokas_by_chapter(chapter_id)
if not slokas:
    st.warning("No slokas for selected chapter.")
    st.stop()

for sloka in slokas:
    with st.container():
        st.markdown(f"<div class='sloka-box'>", unsafe_allow_html=True)
        st.subheader(f"Sloka {sloka['sloka_number']}")
        st.write(sloka.get("sloka_text_telugu", ""))
        st.write(f"**Meaning (Telugu):** {sloka.get('meaning_telugu','')}")
        st.write(f"**Meaning (English):** {sloka.get('meaning_english','')}")
        # Audio playback
        ref_url = sloka.get("reference_audio_url")
        if ref_url:
            st.audio(ref_url, format="audio/mp3")
        else:
            st.info("No reference audio available.")

        # Submission expander + form
        with st.expander("🎤 Submit your recitation/explanation"):
            with st.form(f"submission_form_{sloka['id']}"):
                rec_file = st.file_uploader("Recitation (mp3/wav)", type=["mp3", "wav"], key=f"rec_{sloka['id']}")
                exp_file = st.file_uploader("Explanation (mp3/wav)", type=["mp3", "wav"], key=f"exp_{sloka['id']}")
                submit_btn = st.form_submit_button("Submit")

                if submit_btn:
                    if not rec_file and not exp_file:
                        st.error("Please upload at least one audio file.")
                    else:
                        try:
                            # Build unique paths
                            rec_url = None
                            exp_url = None
                            bucket = "audio"  # ensure this bucket exists in your Supabase storage

                            if rec_file:
                                rec_name = f"user_submissions/{user['id']}/rec_{sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}{os.path.splitext(rec_file.name)[1]}"
                                # upload via public client (db_manager.supabase)
                                db_manager.supabase.storage.from_(bucket).upload(rec_name, rec_file.read())
                                rec_url = f"{db_manager.supabase.storage.url}/{bucket}/{rec_name}" if hasattr(db_manager.supabase.storage, "url") else db_manager.supabase.storage.from_(bucket).get_public_url(rec_name)

                            if exp_file:
                                exp_name = f"user_submissions/{user['id']}/exp_{sloka['id']}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex}{os.path.splitext(exp_file.name)[1]}"
                                db_manager.supabase.storage.from_(bucket).upload(exp_name, exp_file.read())
                                exp_url = f"{db_manager.supabase.storage.url}/{bucket}/{exp_name}" if hasattr(db_manager.supabase.storage, "url") else db_manager.supabase.storage.from_(bucket).get_public_url(exp_name)

                            # Save DB row (use admin to avoid RLS issues on server)
                            db_manager.create_user_submission(user_id=user['id'], sloka_id=sloka['id'], recitation_audio_url=rec_url, explanation_audio_url=exp_url)
                            st.success("✅ Submission saved. Thank you!")
                        except Exception as e:
                            st.error(f"Submission failed: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
