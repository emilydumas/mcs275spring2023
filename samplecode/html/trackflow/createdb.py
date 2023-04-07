"Initialize the database"
import sqlite3
import time

DB_FILE = "trackflow.sqlite"

create_query = """
CREATE TABLE IF NOT EXISTS orders (
    woid INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    assigned_user TEXT,
    created_ts REAL NOT NULL,
    assigned_ts REAL,
    completed_ts REAL,
    CHECK (
        (assigned_user IS NULL AND assigned_ts IS NULL) OR
        (assigned_user IS NOT NULL AND assigned_ts IS NOT NULL)
    )
);
"""

con = sqlite3.connect(DB_FILE)
con.execute(create_query)

con.execute("DELETE FROM orders;")

sample_data = [
    ("Do laundry",time.time()-3600,"ddumas",time.time()),
    ("Post sample code",time.time()+1800,None,None),
]

for t in sample_data:
    con.execute(
        "INSERT INTO orders (description, created_ts, assigned_user, assigned_ts) VALUES (?,?,?,?);",
        t
    )

con.commit() # write queries are discarded unless you do this
con.close()
