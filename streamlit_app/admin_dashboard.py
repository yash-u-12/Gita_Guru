import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_utils import db_manager

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        text-align: center;
        color: #d63384;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .submission-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #d63384;
    }
    .status-submitted { border-left-color: #ffc107; }
    .status-approved { border-left-color: #28a745; }
    .status-rejected { border-left-color: #dc3545; }
    .audio-player {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="admin-header">⚙️ Gita Guru Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # Admin authentication (simple password check)
    if not check_admin_auth():
        return
    
    # Sidebar navigation
    st.sidebar.title("Admin Panel")
    page = st.sidebar.selectbox(
        "Choose a section",
        ["Review Submissions", "View Statistics", "Manage Content"]
    )
    
    if page == "Review Submissions":
        show_review_submissions()
    elif page == "View Statistics":
        show_statistics()
    elif page == "Manage Content":
        show_manage_content()

def check_admin_auth():
    """Simple admin authentication"""
    st.sidebar.markdown("### Admin Login")
    
    # In a real application, you'd want proper authentication
    # For demo purposes, using a simple password
    password = st.sidebar.text_input("Admin Password", type="password")
    
    if password == "admin123":  # Change this to a secure password
        st.sidebar.success("✅ Admin authenticated")
        return True
    elif password:
        st.sidebar.error("❌ Invalid password")
        return False
    else:
        return False

def show_review_submissions():
    st.header("📋 Review User Submissions")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Submitted", "Approved", "Rejected"]
        )
    
    with col2:
        # Get all chapters for filtering
        chapters = db_manager.get_all_chapters()
        chapter_filter = st.selectbox(
            "Filter by Chapter",
            ["All"] + [f"Chapter {c['chapter_number']}: {c['chapter_name']}" for c in chapters]
        )
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get submissions based on filters
    submissions = get_filtered_submissions(status_filter, chapter_filter)
    
    if not submissions:
        st.info("No submissions found matching the criteria.")
        return
    
    # Display submissions
    for submission in submissions:
        display_submission_card(submission)

def get_filtered_submissions(status_filter, chapter_filter):
    """Get submissions based on filters"""
    try:
        # Get all submissions with user and sloka details
        query = """
        SELECT 
            us.*,
            u.name as user_name,
            u.email as user_email,
            s.sloka_number,
            s.sloka_text_telugu,
            c.chapter_number,
            c.chapter_name
        FROM user_submissions us
        JOIN users u ON us.user_id = u.id
        JOIN slokas s ON us.sloka_id = s.id
        JOIN chapters c ON s.chapter_id = c.id
        """
        
        # Apply filters
        if status_filter != "All":
            query += f" WHERE us.status = '{status_filter}'"
        
        # This is a simplified approach - in production, you'd use proper SQL filtering
        submissions = db_manager.supabase.table('user_submissions').select(
            '*, users(name, email), slokas(sloka_number, sloka_text_telugu), chapters(chapter_number, chapter_name)'
        ).execute()
        
        filtered_submissions = []
        for submission in submissions.data:
            # Apply status filter
            if status_filter != "All" and submission['status'] != status_filter:
                continue
            
            # Apply chapter filter
            if chapter_filter != "All":
                chapter_info = f"Chapter {submission['chapters']['chapter_number']}: {submission['chapters']['chapter_name']}"
                if chapter_info != chapter_filter:
                    continue
            
            filtered_submissions.append(submission)
        
        return filtered_submissions
        
    except Exception as e:
        st.error(f"Error fetching submissions: {e}")
        return []

def display_submission_card(submission):
    """Display a submission card for review"""
    status = submission['status']
    status_color = {
        'Submitted': 'warning',
        'Approved': 'success', 
        'Rejected': 'danger'
    }.get(status, 'secondary')
    
    st.markdown(f"""
    <div class="submission-card status-{status.lower()}">
        <h4>Submission by {submission['users']['name']} ({submission['users']['email']})</h4>
        <p><strong>Chapter:</strong> {submission['chapters']['chapter_number']}: {submission['chapters']['chapter_name']}</p>
        <p><strong>Sloka:</strong> {submission['slokas']['sloka_number']}</p>
        <p><strong>Status:</strong> <span class="badge bg-{status_color}">{status}</span></p>
        <p><strong>Submitted:</strong> {submission['created_at'][:19]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio players
    if submission['recitation_audio_url']:
        st.markdown("**Recitation Audio:**")
        st.audio(submission['recitation_audio_url'])
    
    if submission['explanation_audio_url']:
        st.markdown("**Explanation Audio:**")
        st.audio(submission['explanation_audio_url'])
    
    # Admin actions
    if status == "Submitted":
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button(f"✅ Approve", key=f"approve_{submission['id']}"):
                update_submission_status(submission['id'], "Approved")
                st.success("Submission approved!")
                st.rerun()
        
        with col2:
            if st.button(f"❌ Reject", key=f"reject_{submission['id']}"):
                update_submission_status(submission['id'], "Rejected")
                st.error("Submission rejected!")
                st.rerun()
        
        with col3:
            admin_notes = st.text_area(
                "Admin Notes (optional)",
                key=f"notes_{submission['id']}",
                placeholder="Add notes for the user..."
            )
            if st.button("💾 Save Notes", key=f"save_notes_{submission['id']}"):
                update_submission_notes(submission['id'], admin_notes)
                st.success("Notes saved!")
    
    # Show existing admin notes
    if submission.get('admin_notes'):
        st.markdown(f"**Admin Notes:** {submission['admin_notes']}")
    
    st.markdown("---")

def update_submission_status(submission_id, status):
    """Update submission status"""
    try:
        result = db_manager.update_submission_status(submission_id, status)
        if result:
            st.success(f"Status updated to {status}")
        else:
            st.error("Failed to update status")
    except Exception as e:
        st.error(f"Error updating status: {e}")

def update_submission_notes(submission_id, notes):
    """Update submission admin notes"""
    try:
        result = db_manager.supabase.table('user_submissions').update({
            'admin_notes': notes
        }).eq('id', submission_id).execute()
        
        if result.data:
            st.success("Notes updated successfully")
        else:
            st.error("Failed to update notes")
    except Exception as e:
        st.error(f"Error updating notes: {e}")

def show_statistics():
    st.header("📊 Submission Statistics")
    
    try:
        # Get basic statistics
        all_submissions = db_manager.supabase.table('user_submissions').select('*').execute()
        submissions = all_submissions.data
        
        if submissions:
            total_submissions = len(submissions)
            submitted_count = len([s for s in submissions if s['status'] == 'Submitted'])
            approved_count = len([s for s in submissions if s['status'] == 'Approved'])
            rejected_count = len([s for s in submissions if s['status'] == 'Rejected'])
            
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Submissions", total_submissions)
            
            with col2:
                st.metric("Pending Review", submitted_count)
            
            with col3:
                st.metric("Approved", approved_count)
            
            with col4:
                st.metric("Rejected", rejected_count)
            
            # Approval rate
            if total_submissions > 0:
                approval_rate = (approved_count / total_submissions) * 100
                st.metric("Approval Rate", f"{approval_rate:.1f}%")
            
            # Recent activity
            st.subheader("Recent Activity")
            recent_submissions = sorted(submissions, key=lambda x: x['created_at'], reverse=True)[:10]
            
            for submission in recent_submissions:
                st.markdown(f"""
                - **{submission['created_at'][:10]}**: {submission['status']} submission 
                  (Chapter {submission.get('chapter_number', 'N/A')}, Sloka {submission.get('sloka_number', 'N/A')})
                """)
        else:
            st.info("No submissions found.")
            
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")

def show_manage_content():
    st.header("🔧 Manage Content")
    
    st.markdown("""
    ### Content Management Options
    
    This section allows administrators to:
    
    - **Add New Chapters**: Upload new chapter data
    - **Update Slokas**: Modify existing sloka information
    - **Manage Audio Files**: Upload or replace reference audio
    - **User Management**: View and manage user accounts
    
    ### Database Operations
    
    - **Backup Database**: Export current data
    - **Restore Database**: Import from backup
    - **Clean Data**: Remove old or invalid records
    
    *Note: These features are under development.*
    """)
    
    # Placeholder for future content management features
    st.info("Content management features will be implemented in future updates.")

if __name__ == "__main__":
    main() 