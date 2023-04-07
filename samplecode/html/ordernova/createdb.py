"Make the ordernova database"
import sqlite3
import time

DB_FILE = "ordernova.sqlite"

create_query = """
CREATE TABLE IF NOT EXISTS orders (
    woid INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    assigned_user TEXT,
    created_ts REAL NOT NULL,
    assigned_ts REAL,
    completed_ts REAL,
    CHECK (
        (assigned_ts IS NULL AND assigned_user IS NULL)
        OR
        (assigned_ts IS NOT NULL AND assigned_user IS NOT NULL)
    )
);"""

con = sqlite3.connect(DB_FILE)
con.execute(create_query)
con.execute("DELETE FROM orders;")

sample_data = [
    ("Do laundry",time.time()-3600),
    ("Post sample code",time.time()+2*3600),
]

for t in sample_data:
    con.execute("INSERT INTO orders (description,created_ts) VALUES (?,?);",
        t
    )

con.commit()
con.close()