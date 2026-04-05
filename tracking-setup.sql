-- Usage tracking for Consumer Safari
CREATE TABLE IF NOT EXISTS usage_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  event_type TEXT NOT NULL,
  event_data JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast queries
CREATE INDEX IF NOT EXISTS idx_usage_events_type ON usage_events(event_type);
CREATE INDEX IF NOT EXISTS idx_usage_events_created ON usage_events(created_at);
CREATE INDEX IF NOT EXISTS idx_usage_events_user ON usage_events(user_id);

-- RLS: anyone can insert (for anonymous tracking), only service role can read
ALTER TABLE usage_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can insert events" ON usage_events FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can view own events" ON usage_events FOR SELECT USING (auth.uid() = user_id);
