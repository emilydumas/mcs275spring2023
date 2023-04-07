# MCS 275 Spring 2023 Lecture 32
"Work order tracker"

import flask
import time
import sqlite3

DB_FILE = "trackflow.sqlite"

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
        (username,)
    )
    #(1,"Do laundry", 67841632) ->
    #{ "woid": 1, "description": "Do laundry", "created_ts": 1237498 }
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
        d = {
            "woid": row[0],
            "description": row[1],
            "created_ts": row[2]
        }
        open_wo_data.append(d)

    con.close()

    # Render the template
    return flask.render_template(
        "tf-workerview.html",  # Name of template file
        username=username,
        assigned_wo_data=assigned_wo_data,
        open_wo_data=open_wo_data
    )


# Run the application
app.run()  # This will never return.  You lose all control over the program.
