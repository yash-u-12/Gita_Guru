-- Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =======================
-- TABLE: CHAPTERS
-- =======================
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_number INTEGER UNIQUE NOT NULL,
    chapter_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =======================
-- TABLE: SLOKAS
-- =======================
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

-- =======================
-- TABLE: USERS
-- =======================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,  -- Must match auth.uid()
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =======================
-- TABLE: USER SUBMISSIONS
-- =======================
CREATE TABLE IF NOT EXISTS user_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    sloka_id UUID REFERENCES slokas(id) ON DELETE CASCADE,
    recitation_audio_url TEXT,
    explanation_audio_url TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Approved', 'Rejected')) DEFAULT 'Submitted',
    admin_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =======================
-- ENABLE RLS
-- =======================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_submissions ENABLE ROW LEVEL SECURITY;

-- =======================
-- RLS POLICIES: USERS
-- =======================
DROP POLICY IF EXISTS "Users can read their own data" ON users;
DROP POLICY IF EXISTS "Users can insert themselves" ON users;

CREATE POLICY "Users can read their own data"
ON users FOR SELECT
USING (id = auth.uid());

CREATE POLICY "Users can insert themselves"
ON users FOR INSERT
WITH CHECK (id = auth.uid());

-- =======================
-- RLS POLICIES: USER SUBMISSIONS
-- =======================
DROP POLICY IF EXISTS "Users can read their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can insert their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can update their own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Users can delete their own submissions" ON user_submissions;

CREATE POLICY "Users can read their own submissions"
ON user_submissions FOR SELECT
USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own submissions"
ON user_submissions FOR INSERT
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own submissions"
ON user_submissions FOR UPDATE
USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own submissions"
ON user_submissions FOR DELETE
USING (user_id = auth.uid());
