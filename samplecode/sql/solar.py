"SQLite example program - this one just adds three rows"
# MCS 275 Spring 2023 Lecture 27

import sqlite3

con = sqlite3.connect("solarsystem.sqlite")  # filename

con.execute(
    """
CREATE TABLE IF NOT EXISTS planets (
  name TEXT,
  dist REAL,
  year_discovered INTEGER
);
"""
)

con.execute("DELETE FROM planets;")  # delete ALL rows in that table

con.execute(
    """
INSERT INTO planets VALUES (?,?,?)
""",
    ("Earth", 1.0, None)  # None -> DB "NULL"
    # name   dist year_discovered
)

con.execute(
    """
INSERT INTO planets VALUES (?,?,?)
""",
    ("Neptune", 30.1, 1846),
)


con.execute(
    """
INSERT INTO planets VALUES (?,?,?)
""",
    ("Jupiter", 5.2, None),
)

res = con.execute("SELECT * FROM planets;")
for row in res:  # res is iterable
    print("name=", row[0], "dist=", row[1], "year_discovered=", row[2])

con.commit()  # write changes to disk
con.close()  # Close the DB file
