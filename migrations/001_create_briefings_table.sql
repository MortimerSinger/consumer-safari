-- Migration: create briefings table for Consumer Safari hardened backend
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/ugmirwqwlggdemwklcwi/sql

CREATE TABLE IF NOT EXISTS public.briefings (
    id          BIGSERIAL PRIMARY KEY,
    date        DATE NOT NULL,
    data        JSONB NOT NULL,
    is_current  BOOLEAN NOT NULL DEFAULT FALSE,
    schema_version INTEGER NOT NULL DEFAULT 1,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS briefings_date_idx ON public.briefings(date DESC);
CREATE INDEX IF NOT EXISTS briefings_current_idx ON public.briefings(is_current) WHERE is_current = TRUE;

-- Only one row can be is_current at a time
CREATE UNIQUE INDEX IF NOT EXISTS briefings_only_one_current
    ON public.briefings(is_current) WHERE is_current = TRUE;

-- RLS: anon can read current briefing only; service_role can do anything
ALTER TABLE public.briefings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon read current briefing" ON public.briefings;
CREATE POLICY "anon read current briefing" ON public.briefings
    FOR SELECT
    TO anon, authenticated
    USING (is_current = TRUE);

DROP POLICY IF EXISTS "service_role full access" ON public.briefings;
CREATE POLICY "service_role full access" ON public.briefings
    FOR ALL
    TO service_role
    USING (TRUE) WITH CHECK (TRUE);

-- Trigger to keep updated_at fresh
CREATE OR REPLACE FUNCTION public.briefings_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS briefings_updated_at ON public.briefings;
CREATE TRIGGER briefings_updated_at
    BEFORE UPDATE ON public.briefings
    FOR EACH ROW
    EXECUTE FUNCTION public.briefings_set_updated_at();
