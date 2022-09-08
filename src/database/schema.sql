-- following conventions @ https://stackoverflow.com/a/2118567
-- sqlite3 mined_vocabulary.sqlite3 < schema.sql

CREATE TABLE IF NOT EXISTS MiningSessions (
    -- automatically autoincrements for a field defined with INTEGER PRIMARY KEY
    SessionId INTEGER PRIMARY KEY NOT NULL,
    Source NVARCHAR,
    Notes NVARCHAR,
    UpdatedAt DATETIME DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS Vocabularies (
    VocabularyId INTEGER PRIMARY KEY NOT NULL,
    Vocabulary NVARCHAR NOT NULL,
    Reading NVARCHAR,
    Meaning NVARCHAR,
    Sentence NVARCHAR,
    Notes NVARCHAR,
    SessionId INTEGER REFERENCES MiningSessions(SessionId) ON DELETE CASCADE
);
