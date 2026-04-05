-- ============================================================
-- TCP Morning Briefing -- Supabase Schema Setup
-- Run this in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/ugmirwqwlggdemwklcwi/sql/new
-- ============================================================

-- Saved articles table
CREATE TABLE IF NOT EXISTS saved_articles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  tag TEXT,
  source TEXT,
  excerpt TEXT,
  saved_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, url)
);

-- Article notes table
CREATE TABLE IF NOT EXISTS article_notes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  article_url TEXT NOT NULL,
  note TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, article_url)
);

-- Enable Row Level Security
ALTER TABLE saved_articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE article_notes ENABLE ROW LEVEL SECURITY;

-- RLS Policies: users can only see/edit their own data
CREATE POLICY "Users can view own saved articles"
  ON saved_articles FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own saved articles"
  ON saved_articles FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own saved articles"
  ON saved_articles FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own notes"
  ON article_notes FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own notes"
  ON article_notes FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own notes"
  ON article_notes FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own notes"
  ON article_notes FOR DELETE USING (auth.uid() = user_id);
