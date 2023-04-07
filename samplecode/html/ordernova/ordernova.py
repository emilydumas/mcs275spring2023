# MCS 275 Spring 2023 Lecture 32
"Work order tracking application"

import flask
import time
import sqlite3

DB_FILE = "ordernova.sqlite"

app = flask.Flask("OrderNova")

# visit localhost:5000/worker/ddumas/
# calls this function as
# workerview("ddumas")

@app.route("/worker/<username>/")
def workerview(username):
    "Render the worker view template based on database queries"
    # Setup
    con = sqlite3.connect(DB_FILE)
    # Determine assigned work orders
    res = con.execute(
        """
        SELECT woid, description, created_ts, assigned_ts
        FROM orders
        WHERE assigned_user=?
        AND completed_ts IS NULL;
        """,
        (username,)
    )
    assigned_wo_data = []
    for row in res:
        d = { 
            "woid": row[0],
            "description": row[1],
            "created_ts": row[2],
            "assigned_ts": row[3]
        }
        assigned_wo_data.append(d)
    # Determine unassigned work orders
    res = con.execute(
        """
        SELECT woid, description, created_ts
        FROM orders
        WHERE assigned_user IS NULL
        AND completed_ts IS NULL;
        """
    )
    open_wo_data = []
    for row in res:
        d = { 
            "woid": row[0],
            "description": row[1],
            "created_ts": row[2],
        }
        open_wo_data.append(d)

    # Teardown
    con.close()

    # Return
    return flask.render_template(
        "on-workerview.html",
        username = username,
        open_wo_data = open_wo_data,
        assigned_wo_data = assigned_wo_data,
    )

# Run the application
app.run()  # This will never return.  You lose all control over the program.
