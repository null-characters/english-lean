-- Migration 001: Add source and tags columns to words table
--
-- Recommended (automatic): any code path that calls init_db() upgrades old DBs, e.g.
--   python -m english_lean.tools.seed <path/to/pack.json>
--   python -m english_lean
-- See english_lean.db.connection._migrate_words_source_tags
--
-- Manual SQL (only if you cannot run the app; DB must still be missing these columns):
--   sqlite3 /path/to/english_lean.db < src/english_lean/db/migrations/001_words_source_tags.sql
--
-- If sqlite3 prints "duplicate column name: source" / "tags": the columns already exist
-- (migration already applied). No further action — your database is up to date.
--
-- New installs: schema.sql already includes these columns; this file is a no-op for them
-- when used manually (same duplicate-column behavior).

-- Add 'source' column: identifies where the word data came from (e.g., 'ecdict', 'netem')
ALTER TABLE words ADD COLUMN source TEXT;

-- Add 'tags' column: JSON array string for filtering (e.g., '["cet4"]', '["kaoyan"]')
-- Note: SQLite stores JSON as TEXT; JSON1 extension can query when enabled.
ALTER TABLE words ADD COLUMN tags TEXT;
