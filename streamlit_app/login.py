import streamlit as st
import sys
import os
import uuid
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import wave, contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from database.db_utils import db_manager

# Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)  # server-side admin checks

# Use your bucket; override with .env SUPABASE_BUCKET if needed
BUCKET_NAME = os.getenv("SUPABASE_BUCKET", "gita-guru")

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Divine Learning Platform",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    .auth-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: 0 auto;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .auth-tabs {
        display: flex;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 2rem;
    }
    
    .auth-tab {
        flex: 1;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .auth-tab.active {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #667eea;
    }
    
    .auth-tab:not(.active) {
        color: #6c757d;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 500;
        color: #495057;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
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
    
    .warning-message {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #dee2e6, transparent);
        margin: 2rem 0;
    }
    
    .features {
        display: flex;
        justify-content: space-around;
        margin-top: 3rem;
        text-align: center;
    }
    
    .feature {
        color: white;
        opacity: 0.8;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <div class="main-title">🕉️ Gita Guru</div>
    <div class="subtitle">Divine Learning Platform</div>
</div>
""", unsafe_allow_html=True)

# Auth container
with st.container():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Tab selection
    col1, col2 = st.columns(2)
    with col1:
        signin_selected = st.button("Sign In", key="signin_tab", use_container_width=True)
    with col2:
        signup_selected = st.button("Sign Up", key="signup_tab", use_container_width=True)
    
    # Default to sign in if no selection
    if not signin_selected and not signup_selected:
        signin_selected = True
    
    # ----------------- SIGN IN -----------------
    if signin_selected:
        st.markdown("### Welcome Back 🙏")
        st.markdown("Sign in to continue your spiritual journey")
        
        with st.form("signin_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Sign In", use_container_width=True)

        if submit:
            if not email or not password:
                st.markdown('<div class="error-message">Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                try:
                    auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                    if auth_response and getattr(auth_response, "user", None):
                        user_obj = auth_response.user
                        user_id = user_obj.id

                        # Use admin client to check users table (bypass RLS) so existing users are detected reliably
                        try:
                            res = admin_client.table("users").select("*").eq("id", user_id).execute()
                            existing = res.data[0] if res.data else None

                            if existing:
                                st.markdown('<div class="success-message">✅ Sign in successful — redirecting...</div>', unsafe_allow_html=True)
                                st.session_state["user"] = {"id": existing["id"], "email": existing["email"], "name": existing["name"]}
                                st.switch_page("pages/user_portal.py")
                                st.rerun()
                            else:
                                # Try to create user profile if it doesn't exist
                                try:
                                    created = db_manager.create_user_if_not_exists(user_id=user_id, name=user_obj.email, email=user_obj.email)
                                    if created:
                                        st.markdown('<div class="success-message">✅ Profile created and sign in successful — redirecting...</div>', unsafe_allow_html=True)
                                        st.session_state["user"] = {"id": created["id"], "email": created["email"], "name": created["name"]}
                                        st.switch_page("pages/user_portal.py")
                                        st.rerun()
                                    else:
                                        st.markdown('<div class="warning-message">⚠️ Could not create user profile. Please contact support.</div>', unsafe_allow_html=True)
                                except Exception as create_error:
                                    st.markdown(f'<div class="error-message">❌ Profile creation failed: {str(create_error)}</div>', unsafe_allow_html=True)
                        except Exception as db_error:
                            st.markdown(f'<div class="error-message">❌ Database error: {str(db_error)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Sign in failed. Check your credentials.</div>', unsafe_allow_html=True)
                except Exception as e:
                    error_msg = str(e)
                    if "Invalid login credentials" in error_msg:
                        st.markdown('<div class="error-message">❌ Invalid email or password. Please check your credentials.</div>', unsafe_allow_html=True)
                    elif "Email not confirmed" in error_msg:
                        st.markdown('<div class="warning-message">📧 Please confirm your email address before signing in.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ Sign in error: {error_msg}</div>', unsafe_allow_html=True)

    # ----------------- SIGN UP -----------------
    else:
        st.markdown("### Join the Journey 🌟")
        st.markdown("Create your account to begin learning")
        
        with st.form("signup_form"):
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
            register = st.form_submit_button("✨ Create Account", use_container_width=True)

        if register:
            if not name or not email or not password:
                st.markdown('<div class="error-message">Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                try:
                    # Create auth user
                    auth_response = supabase.auth.sign_up({"email": email, "password": password})

                    if auth_response and getattr(auth_response, "user", None):
                        user_id = auth_response.user.id
                        
                        # Check if email confirmation is required
                        if hasattr(auth_response, 'session') and auth_response.session is None:
                            st.markdown('<div class="warning-message">📧 Please check your email and confirm your account before signing in.</div>', unsafe_allow_html=True)
                            st.markdown('<div class="info-message">After confirming your email, you can sign in with your credentials.</div>', unsafe_allow_html=True)
                        else:
                            # Create user row if not exists — use admin to check/insert
                            try:
                                created = db_manager.create_user_if_not_exists(user_id=user_id, name=name, email=email)
                                
                                if created:
                                    # Save session state and proceed
                                    st.markdown('<div class="success-message">✅ Account created successfully! Welcome to Gita Guru.</div>', unsafe_allow_html=True)
                                    st.session_state["user"] = {"id": created["id"], "email": email, "name": name}
                                    
                                    st.switch_page("pages/user_portal.py")
                                    st.rerun()
                                else:
                                    st.markdown('<div class="error-message">❌ User profile creation failed. Please try again.</div>', unsafe_allow_html=True)
                            except Exception as db_error:
                                st.markdown(f'<div class="error-message">❌ Database error: {str(db_error)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Sign up failed. Please try again.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-message">❌ Sign up failed: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("""
<div class="features">
    <div class="feature">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Sacred Texts</div>
        <div class="feature-desc">Learn from ancient wisdom</div>
    </div>
    <div class="feature">
        <div class="feature-icon">🎤</div>
        <div class="feature-title">Audio Learning</div>
        <div class="feature-desc">Listen and practice</div>
    </div>
    <div class="feature">
        <div class="feature-icon">🌟</div>
        <div class="feature-title">Spiritual Growth</div>
        <div class="feature-desc">Transform your life</div>
    </div>
</div>
""", unsafe_allow_html=True)
