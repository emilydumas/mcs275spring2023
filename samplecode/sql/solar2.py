"""
Generate tiny sqlite database of planet data
more complete than the one we'll prepare live
in lecture 27.
"""
# Note: All the "IF NOT EXISTS" in these SQL commands make it
# so the program won't raise an exception if the database file
# already exists.
import sqlite3

con = sqlite3.connect("solarsystem.sqlite")  # .db also popular
con.execute(
    """CREATE TABLE IF NOT EXISTS planets (
            name TEXT,
            dist REAL, 
            year_discovered INTEGER
        );"""
)
# In case the table already exists, delete all its rows.
con.execute("DELETE FROM planets;")
# List of tuples to add
planetdata = [
    ("Mercury", 0.4, None),
    ("Venus", 0.7, None),
    ("Earth", 1.0, None),
    ("Mars", 1.5, None),
    ("Jupiter", 5.2, None),
    ("Saturn", 9.5, None),
    ("Uranus", 19.2, 1781),
    ("Neptune", 30.1, 1846),
]
# Loop to add each tuple as a row of the table
for row in planetdata:
    con.execute("INSERT INTO planets VALUES (?,?,?);", row)

con.commit()  # Save any changes to disk
con.close()  # Close the database file
