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


def db_create_tables(c):
    "Make the tables with connection `c`"
    c.execute(create_query)


def db_clear_tables(c):
    "Remove all work orders with connection `c`"
    c.execute("DELETE FROM orders;")


def db_add_sample_data(c):
    "Add sample rows to orders table with connection `c`"
    sample_data = [
        ("Repair projector in LCA A002", 1679940303.0, None, None),
        ("Post sample code", 1680876033.0, "ddumas", 1680894498.0),
    ]

    for t in sample_data:
        c.execute(
            "INSERT INTO orders (description, created_ts, assigned_user, assigned_ts) VALUES (?,?,?,?);",
            t,
        )


if __name__ == "__main__":
    con = sqlite3.connect(DB_FILE)

    db_create_tables(con)
    db_clear_tables(con)
    db_add_sample_data(con)

    con.commit()  # write queries are discarded unless you do this
    con.close()
