PRAGMA foreign_keys = ON;

-- Categories lookup table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Models lookup table
CREATE TABLE IF NOT EXISTS models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL UNIQUE,
    provider TEXT,
    model_version TEXT,
    notes TEXT
);

-- Conversations lookup table
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id INTEGER PRIMARY KEY,
    started_at TEXT NOT NULL,
    title TEXT,
    source TEXT,
    notes TEXT
);

-- Label definitions
CREATE TABLE IF NOT EXISTS labels (
    label_id INTEGER PRIMARY KEY,
    label_name TEXT NOT NULL UNIQUE,
    status BOOLEAN, -- 1.0 is a pass, 0.0 is any of the fails
    severity INTEGER,
    description TEXT
);

-- Prompts table
CREATE TABLE IF NOT EXISTS prompts (
    prompt_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    model_id INTEGER NOT NULL,
    conversation_id INTEGER NOT NULL,
    prompt_number INTEGER NOT NULL,
    prompt_text TEXT NOT NULL,
    raw_output TEXT,
    label_id INTEGER,


    -- Metadata
    source TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(category_id)
        REFERENCES categories(category_id),

    FOREIGN KEY(model_id)
        REFERENCES models(model_id),

    FOREIGN KEY(conversation_id)
        REFERENCES conversations(conversation_id),

    FOREIGN KEY(label_id)
        REFERENCES labels(label_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_prompt_category
ON prompts(category_id);

CREATE INDEX IF NOT EXISTS idx_prompt_model
ON prompts(model_id);

CREATE INDEX IF NOT EXISTS idx_prompt_conversation
ON prompts(conversation_id);

CREATE INDEX IF NOT EXISTS idx_prompt_category_model
ON prompts(category_id, model_id);

CREATE INDEX IF NOT EXISTS idx_prompt_created
ON prompts(created_at);

CREATE INDEX IF NOT EXISTS idx_labels_status
ON labels(status);

CREATE INDEX IF NOT EXISTS idx_prompt_label
ON prompts(label_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_prompt_number
ON prompts(conversation_id, prompt_number, model_id);
