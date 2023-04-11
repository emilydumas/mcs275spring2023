# MCS 275 Spring 2023 Lecture 32
"Work order tracking application"

import flask
import time
import sqlite3
import os

import createdb
from createdb import DB_FILE

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
        (username,),
    )
    assigned_wo_data = []
    for row in res:
        d = {
            "woid": row[0],
            "description": row[1],
            "created_ts": row[2],
            "assigned_ts": row[3],
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
        username=username,
        open_wo_data=open_wo_data,
        assigned_wo_data=assigned_wo_data,
    )

# The route to DISPLAY the form
@app.route("/new/")
def new_work_order():
    "Show the new work order form"
    return flask.render_template("on-neworder.html")

# The route to handle SUBMISSION of the form
@app.route("/new/submit", methods = ["POST", "GET"])
def create_work_order():
    "Create a new work order"
    # Retreive form data from flask
    #username = flask.request.values.get("username")
    description = flask.request.values.get("description")
    # Setup
    con = sqlite3.connect(DB_FILE)
    # Determine assigned work orders
    res = con.execute(
        """
        INSERT INTO orders (description,created_ts)
        VALUES (?,?);
        """,
        (description,time.time()),
    )
    con.commit()
    con.close()
    
    return flask.redirect("/new/") # instruct the browser to go back to /new/

@app.route("/wo/<int:woid>/assign_to/<username>/")
def assign(woid,username):
    "Assign a work order to a user"
    # Setup
    con = sqlite3.connect(DB_FILE)
    # Determine assigned work orders
    res = con.execute(
        """
        UPDATE orders
        SET assigned_user=?, assigned_ts=?
        WHERE woid=?;
        """,
        (username,time.time(),woid),
    )
    # TODO: Tell the user whether this query actually affected any rows
    con.commit()
    con.close()
    
    return flask.redirect("/worker/{}/".format(username)) # instruct the browser to go back to /new/


# The URL to assign work order 3 to user ddumas will be
# /wo/3/assign_to/ddumas/

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
