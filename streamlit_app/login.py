import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from database.db_utils import db_manager

# Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)  # server-side admin checks

st.set_page_config(page_title="Gita Guru - Sign In / Sign Up", page_icon="🔐")
st.title("🔐 Gita Guru")

mode = st.radio("Choose:", ["Sign In", "Sign Up"], horizontal=True)

# ----------------- SIGN IN -----------------
if mode == "Sign In":
    with st.form("signin_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

    if submit:
        try:
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            if auth_response and getattr(auth_response, "user", None):
                user_obj = auth_response.user
                user_id = user_obj.id

                # Use admin client to check users table (bypass RLS) so existing users are detected reliably
                res = admin_client.table("users").select("*").eq("id", user_id).execute()
                existing = res.data[0] if res.data else None

                if existing:
                    st.success("✅ Sign in successful — redirecting...")
                    st.session_state["user"] = {"id": existing["id"], "email": existing["email"], "name": existing["name"]}
                      # rerun to allow other pages to detect session (or switch_page)
                    st.switch_page("pages/user_portal.py")  # or use switch_page if you have that set up
                    st.rerun()
                else:
                    st.warning("⚠️ No profile row found in users table. Please sign up to create a profile.")
            else:
                st.error("❌ Sign in failed. Check credentials.")
        except Exception as e:
            st.error(f"Sign in error: {e}")

# ----------------- SIGN UP -----------------
else:
    with st.form("signup_form"):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        register = st.form_submit_button("Sign Up")

    if register:
        try:
            # Create auth user
            auth_response = supabase.auth.sign_up({"email": email, "password": password})

            if auth_response and getattr(auth_response, "user", None):
                user_id = auth_response.user.id

                # Create user row if not exists — use admin to check/insert
                created = db_manager.create_user_if_not_exists(user_id=user_id, name=name, email=email)

                # Save session state and proceed
                st.success("✅ Account created. You can now sign in.")
                st.session_state["user"] = {"id": created["id"] if created else user_id, "email": email, "name": name}
                
                st.switch_page("pages/user_portal.py")
                st.rerun()
            else:
                st.error("❌ Sign up failed. Try again.")
        except Exception as e:
            st.error(f"Sign up failed: {e}")
