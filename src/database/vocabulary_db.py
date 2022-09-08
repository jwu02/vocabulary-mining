import sqlite3
from pathlib import Path

def connect() -> sqlite3.Connection:
    try:
        db_dir = Path(__file__).parent.resolve()
        connection = sqlite3.connect(Path.joinpath(db_dir, 'mined_vocabulary.sqlite3'))
        connection.execute('PRAGMA foreign_keys = ON') # to enable on delete cascade
    except sqlite3.Error as e:
        print(e)

    # print("Opened connection to database.")

    return connection
