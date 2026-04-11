-- english-lean vocabulary and SRS progress (offline)
-- Timestamps stored as ISO 8601 text (local naive or UTC — app convention).

CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lemma TEXT NOT NULL UNIQUE,
    phonetic TEXT,
    definition_zh TEXT,
    example TEXT,
    morphemes TEXT,
    synonyms TEXT,
    frequency_rank INTEGER,
    source TEXT,
    tags TEXT
);

CREATE TABLE IF NOT EXISTS progress (
    word_id INTEGER PRIMARY KEY REFERENCES words(id) ON DELETE CASCADE,
    ease_factor REAL NOT NULL DEFAULT 2.5,
    interval_days INTEGER NOT NULL DEFAULT 0,
    repetitions INTEGER NOT NULL DEFAULT 0,
    next_review_at TEXT,
    last_reviewed_at TEXT,
    lapses INTEGER NOT NULL DEFAULT 0,
    created_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_progress_next ON progress(next_review_at);
CREATE INDEX IF NOT EXISTS idx_words_lemma ON words(lemma);

-- Daily new-word quota and future stats (key/value, tasks_08 T8.2+)
CREATE TABLE IF NOT EXISTS study_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
