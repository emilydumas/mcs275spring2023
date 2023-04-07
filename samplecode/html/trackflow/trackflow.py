# MCS 275 Spring 2023 Lecture 32
"Work order tracker"

import flask
import time
import sqlite3
import os

import createdb
from createdb import DB_FILE

# Create Flask (application) object
app = flask.Flask("TrackFlow")

# Visiting
# localhost:5000/worker/ddumas/
# will call
# workerview("ddumas")


@app.route("/worker/<username>/")
def workerview(username):
    # DB stuff
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    res = con.execute(
        """
        SELECT woid, description, created_ts, assigned_ts
        FROM orders
        WHERE assigned_user=? AND completed_ts IS NULL;
        """,
        (username,),
    )
    # Convert from an iterable of tuples to a list of dicts
    # (1,"Do laundry", 67841632) ->
    # { "woid": 1, "description": "Do laundry", "created_ts": 1237498 }
    assigned_wo_data = []
    for row in res:
        d = {
            "woid": row[0],
            "description": row[1],
            "created_ts": row[2],
            "assigned_ts": row[3],
        }
        assigned_wo_data.append(d)

    # Get all work orders not yet assigned to anyone
    res = con.execute(
        """
        SELECT woid, description, created_ts
        FROM orders
        WHERE assigned_ts IS NULL AND completed_ts IS NULL;
        """,
    )
    open_wo_data = []
    for row in res:
        d = {"woid": row[0], "description": row[1], "created_ts": row[2]}
        open_wo_data.append(d)

    con.close()

    # Render the template
    return flask.render_template(
        "tf-workerview.html",  # Name of template file
        username=username,
        assigned_wo_data=assigned_wo_data,
        open_wo_data=open_wo_data,
    )


# Make sure database exists
add_sample_data = False
if not os.path.exists(DB_FILE):
    print("The database '{}' was not found.  Creating it.".format(DB_FILE))
    add_sample_data = True

con = sqlite3.connect(DB_FILE)

print("Making sure the DB contains the necessary tables...", end="")
createdb.db_create_tables(con)
print("Done")

if add_sample_data:
    print("Populating DB with sample data, since it was empty...", end="")
    createdb.db_add_sample_data(con)
    print("Done")

con.commit()
con.close()

# Run the application
app.run()  # This will never return.  You lose all control over the program.
