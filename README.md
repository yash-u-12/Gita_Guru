# 🕉️ Gita Guru - Bhagavad Gita Learning Platform

A comprehensive full-stack learning platform for studying the Bhagavad Gita with interactive audio features.

## 🌟 Features

### For Users
- **📖 Complete Sloka Text** in Telugu
- **🎵 Reference Audio** for proper pronunciation
- **📝 Dual Meanings** in Telugu and English
- **📤 Interactive Learning** through audio submissions
- **📊 Progress Tracking** with submission history

### For Admins
- **📋 Review Submissions** with audio playback
- **✅ Approve/Reject** user submissions
- **📝 Add Admin Notes** for feedback
- **📊 View Statistics** and analytics
- **🔧 Content Management** tools

## 🛠️ Tech Stack

- **Backend**: Python, Supabase (PostgreSQL + Storage)
- **Frontend**: Streamlit
- **Database**: PostgreSQL (via Supabase)
- **Storage**: Supabase Storage
- **Authentication**: Email-based user system

## 📁 Project Structure

```
Gita_Guru/
├── config.py                          # Configuration settings
├── requirements.txt                   # Python dependencies
├── setup.py                          # Complete setup script
├── README.md                         # This file
├── database/
│   ├── schema.sql                    # Database schema
│   └── db_utils.py                   # Database utilities
├── scripts/
│   ├── bulk_audio_uploader.py        # Upload audio files
│   ├── db_populator.py               # Populate database
│   └── db_audio_url_updater.py       # Update audio URLs
├── streamlit_app/
│   ├── user_portal.py                # Main user interface
│   └── admin_dashboard.py            # Admin interface
└── slokas/                           # Audio files (your data)
    ├── 12/                           # Chapter 12 audio files
    ├── 15/                           # Chapter 15 audio files
    └── 16/                           # Chapter 16 audio files
```

## 🚀 Quick Setup

### Prerequisites
1. **Supabase Project**: Create a project at [supabase.com](https://supabase.com)
2. **Python 3.8+**: Ensure Python is installed
3. **Audio Files**: Place MP3 files in `slokas/` folder structure
4. **JSON Data**: Ensure chapter JSON files are available

### Step 1: Clone and Install
```bash
# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup
1. Go to your Supabase project SQL editor
2. Copy and run the contents of `database/schema.sql`
3. This creates all necessary tables and indexes

### Step 3: Run Complete Setup
```bash
python setup.py
```

This script will:
- ✅ Install all dependencies
- ✅ Populate database with JSON data
- ✅ Upload all audio files to Supabase Storage
- ✅ Link audio URLs to database records

### Step 4: Launch Applications

**User Portal:**
```bash
streamlit run streamlit_app/user_portal.py
```

**Admin Dashboard:**
```bash
streamlit run streamlit_app/admin_dashboard.py
```

## 📖 Usage Guide

### For Users

1. **Browse Chapters**: Select any chapter from the dropdown
2. **Choose Slokas**: Pick specific slokas to study
3. **Listen & Learn**: Play reference audio and read meanings
4. **Practice**: Upload your own recitation and explanation
5. **Track Progress**: Monitor your submissions and feedback

### For Admins

1. **Access Dashboard**: Use password `admin123`
2. **Review Submissions**: Listen to user audio files
3. **Take Action**: Approve, reject, or add notes
4. **View Statistics**: Monitor platform usage

## 🔧 Manual Setup (Alternative)

If you prefer to run scripts individually:

### 1. Database Population
```bash
python scripts/db_populator.py
```

### 2. Audio Upload
```bash
python scripts/bulk_audio_uploader.py
```

### 3. Audio URL Updates
```bash
python scripts/db_audio_url_updater.py
```

## 📊 Database Schema

### Tables
- **chapters**: Chapter information (id, chapter_number, chapter_name)
- **slokas**: Sloka details (id, chapter_id, sloka_number, text, meanings, audio_url)
- **users**: User accounts (id, name, email)
- **user_submissions**: User audio submissions (id, user_id, sloka_id, audio_urls, status)

### Relationships
- Chapters → Slokas (one-to-many)
- Users → Submissions (one-to-many)
- Slokas → Submissions (one-to-many)

## 🎵 Audio File Structure

```
slokas/
├── 12/                    # Chapter 12
│   ├── 1.mp3             # Sloka 1
│   ├── 2.mp3             # Sloka 2
│   └── ...
├── 15/                    # Chapter 15
│   ├── 1.mp3
│   └── ...
└── 16/                    # Chapter 16
    ├── 1.mp3
    └── ...
```

## 📝 JSON Data Format

Each chapter JSON file should contain:
```json
[
  {
    "chapter": 12,
    "chapter_name": "భక్తియోగము",
    "sloka_number": "1",
    "sloka_text": "ఏవం సతతయుక్తా యే...",
    "telugu_meaning": "అర్జునుడు పలికెను...",
    "english_meaning": "Arjuna said...",
    "audio_link": ""  // Ignored - will be updated automatically
  }
]
```

## 🔒 Security Notes

- **Admin Password**: Change `admin123` in production
- **API Keys**: Store Supabase credentials securely
- **File Uploads**: Validate audio files before processing
- **User Data**: Implement proper authentication for production

## 🚀 Deployment

### Local Development
```bash
# Run user portal
streamlit run streamlit_app/user_portal.py --server.port 8501

# Run admin dashboard
streamlit run streamlit_app/admin_dashboard.py --server.port 8502
```

### Production Deployment
1. **Streamlit Cloud**: Deploy directly to Streamlit Cloud
2. **Heroku**: Use Procfile and requirements.txt
3. **AWS/GCP**: Containerize with Docker

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify Supabase URL and key in `config.py`
   - Check if database schema is created

2. **Audio Upload Failures**
   - Ensure audio files are valid MP3 format
   - Check Supabase Storage permissions
   - Verify file paths are correct

3. **Streamlit App Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Verify file paths and imports

### Debug Mode
```bash
# Run with debug output
python -u scripts/bulk_audio_uploader.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bhagavad Gita text and translations
- Supabase for backend services
- Streamlit for the web framework
- All contributors and users

## 📞 Support

For support or questions:
- Create an issue on GitHub
- Contact the development team
- Check the troubleshooting section

---

**🕉️ Happy Learning! May the wisdom of the Bhagavad Gita guide your journey.** 