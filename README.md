## TodoList
- output command line prints to a label on top of main body
    - remove excessive prints
- scrape vocabulary details before saving to db
- update database on vocabulary detail fields change

## Commands
- `cd src/database` from root
- `sqlite3 mined_vocabulary.sqlite3 < schema.sql` to create database
- `sqlite3 mined_vocabulary.sqlite3 < seed.sql` to populate database with dummy data
- `python src/main.py` to run program from root