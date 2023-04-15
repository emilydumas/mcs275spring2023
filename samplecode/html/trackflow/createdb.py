"Initialize the database"
import sqlite3
import datetime

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
        (
            "Respond to student emails about Project 4",
            datetime.datetime(2023, 4, 15, 13, 28, 0).timestamp(),
            "ddumas",
            datetime.datetime(2023, 4, 15, 12, 8, 5).timestamp(),
            None,
        ),
        (
            "Finish grading homework 13",
            datetime.datetime(2023, 4, 14, 9, 15, 53).timestamp(),
            None,
            None,
            None,
        ),
        (
            "Finish grading homework 12",
            datetime.datetime(2023, 4, 7, 17, 8, 19).timestamp(),
            "jjoyce",
            datetime.datetime(2023, 4, 8, 12, 3, 2).timestamp(),
            datetime.datetime(2023, 4, 13, 8, 44, 0).timestamp(),
        ),
        (
            "Investigate reports of feral hogs living in SCE basement",
            datetime.datetime(2023, 2, 1, 7, 51, 30).timestamp(),
            None,
            None,
            None,
        ),
        (
            "Distribute flyer about pair of pet pigs lost on campus",
            datetime.datetime(2022, 5, 3, 10, 4, 48).timestamp(),
            None,
            None,
            None,
        ),
    ]

    for t in sample_data:
        c.execute(
            "INSERT INTO orders (description, created_ts, assigned_user, assigned_ts, completed_ts) VALUES (?,?,?,?,?);",
            t,
        )


if __name__ == "__main__":
    con = sqlite3.connect(DB_FILE)

    db_create_tables(con)
    db_clear_tables(con)
    db_add_sample_data(con)

    con.commit()  # write queries are discarded unless you do this
    con.close()
