# MCS 275 Spring 2023 Lecture 32
"Work order tracker"

import flask
import time
import sqlite3
import os
import timefmt

import createdb
from createdb import DB_FILE

# Create Flask (application) object
app = flask.Flask("TrackFlow")

@app.route("/")
def show_front():
    "Show a simple, unstyled front page"
    return """<!doctype html>
<html>
<head><title>TrackFlow front page</title><style>body { max-width: 48rem; margin: auto; padding: 1rem; }</style></head>
<body>
<p>Try these URLs to demonstrate the application.</p>
<ul>
    <li><a href="/new/"><code>/new/</code>: Make a new work order</a></li>
    <li><a href="/worker/ddumas/"><code>/worker/ddumas/</code>: Show worker view for a given user (ddumas)</a></li>
    <li><a href="/worker/ghopper/"><code>/worker/ghopper/</code>: Show worker view for a given user (ghopper)</a></li>
    <li><a href="/wo/1/"><code>/wo/1/</code>: Show details of a work order by number (1)</a></li>
</body>
</html>
"""

# Visiting
# localhost:5000/worker/ddumas/
# will call
# workerview("ddumas")

@app.route("/new/")
def show_new_order_form():
    "Display the work order creation form"
    return flask.render_template("tf-neworder.html")

@app.route("/new/submit", methods=["GET","POST"])  # GET-only is default
def create_new_order():
    "Create a new work order based on information submitted in a form"
    # Retrieve form data
    username = flask.request.values.get("username")
    description = flask.request.values.get("description")
    # Use form data
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    con.execute(
        """
        INSERT INTO orders (description, created_ts)
        VALUES (?,?);
        """,
        (description, time.time()),
    )
    # Now determine the ID of the row we just created.
    res = con.execute("SELECT last_insert_rowid();")
    woid = res.fetchone()[0]
    
    con.commit()
    con.close()
    return flask.redirect("/wo/{}/".format(woid))

@app.route("/worker/<username>/")
def workerview(username):
    now = time.time()

    # DB stuff
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    res = con.execute(
        """
        SELECT woid, description, created_ts, assigned_ts
        FROM orders
        WHERE assigned_user=? AND completed_ts IS NULL
        ORDER BY assigned_ts;
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
        d["assigned_ts_str"] = timefmt.ts_fmt(d["assigned_ts"])
        d["assigned_ts_ago"] = timefmt.tsdiff_fmt(now-d["assigned_ts"])

        assigned_wo_data.append(d)

    # Get all work orders not yet assigned to anyone
    res = con.execute(
        """
        SELECT woid, description, created_ts
        FROM orders
        WHERE assigned_ts IS NULL AND completed_ts IS NULL
        ORDER BY created_ts;
        """,
    )
    open_wo_data = []
    for row in res:
        d = {"woid": row[0], "description": row[1], "created_ts": row[2]}
        d["created_ts_str"] = timefmt.ts_fmt(d["created_ts"])
        d["created_ts_ago"] = timefmt.tsdiff_fmt(now-d["created_ts"])
        open_wo_data.append(d)

    con.close()

    # Render the template
    return flask.render_template(
        "tf-workerview.html",  # Name of template file
        username=username,
        assigned_wo_data=assigned_wo_data,
        open_wo_data=open_wo_data,
    )

@app.route("/wo/<int:woid>/")
def show_work_order(woid):
    "Display a page of info about existing work order"
    con = sqlite3.connect(DB_FILE)
    res = con.execute(
        """
        SELECT description, assigned_user, created_ts, assigned_ts, completed_ts
        FROM orders
        WHERE woid=?
        """,
        (woid,),
    )
    result_rows = res.fetchall()
    con.close()

    if not result_rows:
        # No row returned: give a 404 Not Found response
        flask.abort(404)
    if len(result_rows) != 1:
        # If multiple rows, give 500 Internal Server Error
        flask.abort(500)

    row = result_rows[0]
    description = row[0]
    assigned_user = row[1]
    created_ts = row[2]
    assigned_ts = row[3]
    completed_ts = row[4]

    created_ts_str = timefmt.ts_fmt(created_ts)

    if assigned_ts:
        assigned_ts_str = timefmt.ts_fmt(assigned_ts)
    else:
        assigned_ts_str = "---"

    if completed_ts:
        completed_ts_str = timefmt.ts_fmt(completed_ts)
    else:
        completed_ts_str = "---"

    return flask.render_template(
        "tf-showorder.html",
        woid=woid,
        description=description,
        created_ts_str=created_ts_str,
        assigned_ts_str=assigned_ts_str,
        completed_ts_str=completed_ts_str,
        assigned_user=assigned_user,
    )

# I want visiting
# /wo/3/assign_to/ddumas/
# to assign work order 3 to user "ddumas"

@app.route("/wo/<int:woid>/assign_to/<username>/")
def assign_work_order_to_user(woid,username):
    "Assign the worker order with id `woid` to user `username`"
    # Use form data
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    res = con.execute(
        """
        UPDATE orders
        SET assigned_user=?, assigned_ts=?
        WHERE woid=?
        AND assigned_ts IS NULL;
        """,
        (username,time.time(),woid),
    )
    # TODO: Figure out how to tell the user whether this action
    # succeeded.
    con.commit()
    con.close()
    
    return flask.redirect("/worker/{}/".format(username))

@app.route("/wo/<int:woid>/complete/<username>/")
def complete_work_order(woid,username):
    "Assign the worker order with id `woid` to user `username`"
    # Use form data
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    res = con.execute(
        """
        UPDATE orders
        SET completed_ts=?
        WHERE woid=?
        AND completed_ts IS NULL;
        """,
        (time.time(),woid),
    )
    # TODO: Figure out how to tell the user whether this action
    # succeeded.
    con.commit()
    con.close()
    
    return flask.redirect("/worker/{}/".format(username))

@app.route("/wo/<int:woid>/cancel/<username>/")
def cancel_work_order_assignment(woid,username):
    "Assign the worker order with id `woid` to user `username`"
    # Use form data
    con = sqlite3.connect(DB_FILE)

    # Get all work orders assigned to this user (and not yet completed)
    res = con.execute(
        """
        UPDATE orders
        SET assigned_ts=NULL, assigned_user=NULL
        WHERE woid=?
        AND completed_ts IS NULL;
        """,
        (woid,),
    )
    # TODO: Figure out how to tell the user whether this action
    # succeeded.
    con.commit()
    con.close()
    
    return flask.redirect("/worker/{}/".format(username))

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
