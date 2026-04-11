-- Migration 001: Add source and tags columns to words table
-- Run this on existing databases to add vocabulary source tracking.
--
-- Usage (for existing databases):
--   sqlite3 /path/to/english_lean.db < src/english_lean/db/migrations/001_words_source_tags.sql
--
-- For new installations, schema.sql already includes these columns.

-- Add 'source' column: identifies where the word data came from (e.g., 'ecdict', 'netem')
ALTER TABLE words ADD COLUMN source TEXT;

-- Add 'tags' column: JSON array string for filtering (e.g., '["cet4"]', '["kaoyan"]', '["cet4","kaoyan"]')
-- Note: SQLite doesn't have native JSON type; we store as TEXT and use JSON1 functions for queries.
ALTER TABLE words ADD COLUMN tags TEXT;
