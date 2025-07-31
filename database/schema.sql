-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================
-- Chapters table
-- =====================
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_number INTEGER UNIQUE NOT NULL,
    chapter_name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- Slokas table
-- =====================
CREATE TABLE IF NOT EXISTS slokas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    sloka_number INTEGER NOT NULL,
    sloka_text_telugu TEXT NOT NULL,
    meaning_telugu TEXT NOT NULL,
    meaning_english TEXT NOT NULL,
    reference_audio_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(chapter_id, sloka_number)
);

-- =====================
-- Users table
-- =====================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- User Submissions table
-- =====================
CREATE TABLE IF NOT EXISTS user_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    sloka_id UUID REFERENCES slokas(id) ON DELETE CASCADE,
    recitation_audio_url TEXT,
    explanation_audio_url TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Approved', 'Rejected')) DEFAULT 'Submitted',
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================
-- Indexes
-- =====================
CREATE INDEX IF NOT EXISTS idx_slokas_chapter_id ON slokas(chapter_id);
CREATE INDEX IF NOT EXISTS idx_slokas_chapter_sloka ON slokas(chapter_id, sloka_number);
CREATE INDEX IF NOT EXISTS idx_user_submissions_user_id ON user_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_submissions_sloka_id ON user_submissions(sloka_id);
CREATE INDEX IF NOT EXISTS idx_user_submissions_status ON user_submissions(status);

-- =====================
-- Updated_at Trigger Function
-- =====================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =====================
-- Triggers for updated_at
-- =====================
DROP TRIGGER IF EXISTS update_chapters_updated_at ON chapters;
CREATE TRIGGER update_chapters_updated_at
BEFORE UPDATE ON chapters
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_slokas_updated_at ON slokas;
CREATE TRIGGER update_slokas_updated_at
BEFORE UPDATE ON slokas
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_submissions_updated_at ON user_submissions;
CREATE TRIGGER update_user_submissions_updated_at
BEFORE UPDATE ON user_submissions
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================
-- Enable Row Level Security (RLS)
-- =====================

-- Users table: Enable RLS and secure access to user data
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read their own data"
ON public.users
FOR SELECT
USING (id = auth.uid());

-- User Submissions table: Enable RLS and secure access to submissions
ALTER TABLE public.user_submissions ENABLE ROW LEVEL SECURITY;

-- SELECT
CREATE POLICY "Users can read their own submissions"
ON public.user_submissions
FOR SELECT
USING (user_id = auth.uid());

-- INSERT
CREATE POLICY "Users can insert their own submissions"
ON public.user_submissions
FOR INSERT
WITH CHECK (user_id = auth.uid());

-- UPDATE
CREATE POLICY "Users can update their own submissions"
ON public.user_submissions
FOR UPDATE
USING (user_id = auth.uid());

-- DELETE (optional - include only if needed)
CREATE POLICY "Users can delete their own submissions"
ON public.user_submissions
FOR DELETE
USING (user_id = auth.uid());
