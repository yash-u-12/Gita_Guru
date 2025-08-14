-- =====================================
-- Enable UUID Extension
-- =====================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================
-- Clear existing policies and triggers
-- =====================================
DROP TRIGGER IF EXISTS set_user_id_trigger ON user_submissions;
DROP FUNCTION IF EXISTS set_user_id();

-- Drop all existing RLS policies
DROP POLICY IF EXISTS "Users can read their own data" ON users;
DROP POLICY IF EXISTS "Users can insert themselves" ON users;
DROP POLICY IF EXISTS "Users can update themselves" ON users;
DROP POLICY IF EXISTS "Users can read their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can insert their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can update their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can delete their own submissions" ON user_submissions;

-- =====================================
-- TABLE: CHAPTERS
-- =====================================
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_number INTEGER UNIQUE NOT NULL,
    chapter_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- TABLE: SLOKAS
-- =====================================
CREATE TABLE IF NOT EXISTS slokas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    sloka_number INTEGER NOT NULL,
    sloka_text_telugu TEXT NOT NULL,
    meaning_telugu TEXT NOT NULL,
    meaning_english TEXT NOT NULL,
    reference_audio_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(chapter_id, sloka_number)
);

-- =====================================
-- TABLE: USERS
-- =====================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- TABLE: USER SUBMISSIONS
-- =====================================
CREATE TABLE IF NOT EXISTS user_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL, -- Remove the foreign key constraint temporarily
    sloka_id UUID REFERENCES slokas(id) ON DELETE CASCADE,
    recitation_audio_url TEXT,
    explanation_audio_url TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Approved', 'Rejected')) DEFAULT 'Submitted',
    admin_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- DISABLE RLS temporarily to test
-- =====================================
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_submissions DISABLE ROW LEVEL SECURITY;
ALTER TABLE chapters DISABLE ROW LEVEL SECURITY;
ALTER TABLE slokas DISABLE ROW LEVEL SECURITY;

-- =====================================
-- STORAGE SETUP
-- =====================================
-- Ensure bucket exists
INSERT INTO storage.buckets (id, name, public)
VALUES ('audio', 'audio', true)
ON CONFLICT (id) DO NOTHING;

-- Clear all storage policies
DROP POLICY IF EXISTS "Users can upload their own audio files" ON storage.objects;
DROP POLICY IF EXISTS "Users can read their own audio files" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete their own audio files" ON storage.objects;
DROP POLICY IF EXISTS "Public can read audio files" ON storage.objects;

-- Simple storage policies
CREATE POLICY "Anyone can upload audio files"
ON storage.objects
FOR INSERT
WITH CHECK (bucket_id = 'audio');

CREATE POLICY "Anyone can read audio files"
ON storage.objects
FOR SELECT
USING (bucket_id = 'audio');

CREATE POLICY "Anyone can delete audio files"
ON storage.objects
FOR DELETE
USING (bucket_id = 'audio');

CREATE POLICY "Anyone can update audio files"
ON storage.objects
FOR UPDATE
USING (bucket_id = 'audio')
WITH CHECK (bucket_id = 'audio');