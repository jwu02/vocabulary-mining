-- sqlite3 mined_vocabulary.sqlite3 < seed.sql

INSERT INTO MiningSessions (Source, Notes) 
VALUES
    ('session1', 'some notes for 1'),
    ('session2', 'some notes for 2'),
    ('session3', 'some notes for 3');

DELETE from Vocabularies;
INSERT INTO Vocabularies (Vocabulary, SessionId)
VALUES
    ('testing', 1),
    ('dummy', 1),
    ('data', 2),
    ('from', 2),
    ('seed', 2),
    ('file', 2),
    ('.sql', 3);