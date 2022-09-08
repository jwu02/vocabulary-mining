## TodoList
- (maybe) delete and re-add only the widgets that need updating
    - less LOC executed
    - no need for refocusing vocab entry LineEdit programmatically
- entry fields for vocab

## Commands
- `sqlite3 mined_vocabulary.sqlite3 < schema.sql` to create database
- `sqlite3 mined_vocabulary.sqlite3 < seed.sql` to populate database with dummy data
- `python src/main.py` to run program