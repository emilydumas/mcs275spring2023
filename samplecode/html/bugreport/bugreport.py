# MCS 275 Spring 2023 Homework 14
"Bug report system"

import flask
import time
import sqlite3
import os

DB_FILE = "bugreport.sqlite"

# Create Flask (application) object
app = flask.Flask("TrackFlow")


@app.route("/")
def show_front():
    "Show a simple front page"
    return """<!doctype html>
<html>
<head><link rel="stylesheet" href="/static/main.css">
<title>Bug Reporter: Home</title></head>
<body>
<h1>Choose action</h1>
<ul>
    <li><a href="/create/"><code>/create/</code>: Make a bug report</a></li>
    <li><a href="/list/"><code>/list/</code>: Show all the bug reports</a></li>
</body>
</html>
"""


@app.route("/create/")
def create_report_form():
    "Display the bug report creation form"
    return """<!doctype html>
<html>
<head><link rel="stylesheet" href="/static/main.css">
<title>Bug Reporter: Create report</title></head>
<body>
<h1>Create a bug report</h1>
    <div>
    <form action="/create/submit" method="POST">
        <p>
        <label for="fullname">Full name</label>
        <input type="text" id="fullname" name="fullname">
        </p>
        <p>
        <label for="description">Description</label>
        <input type="text" id="description" name="description" size="72">
        </p>  
        <p>
        <label for="severity">Severity level:</label>
        <select name="severity" id="severity">
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
            <option value="critical">critical</option>
        </select>
        </p>
        <input type="submit" value="Create">
    </form>
</div>
</body>
</html>"""


@app.route("/create/submit", methods=["GET", "POST"])  # GET-only is default
def create_report_submission():
    "Create a bug report based on information submitted in the form"
    # ADD THE BODY OF THIS FUNCTION!!


@app.route("/create/done")
def create_report_completed():
    "Tell the user the action was completed"
    return """<!doctype html>
<html>
<head><link rel="stylesheet" href="/static/main.css">
<title>Bug Reporter: Report created</title></head>
<body>
<h1>Done</h1>
<p>The bug report has been created.  What would you like to do next?</p>
<ul>
    <li><a href="/create/">Submit another report</a></li>
    <li><a href="/list/">Go to the list of all bug reports</a></li>
</ul>
</body>
</html>"""


@app.route("/list/")
def report_list():
    "Get and render the list of all bug reports"
    con = sqlite3.connect(DB_FILE)
    res = con.execute(
        """
        SELECT id, created_ts, fullname, description, severity
        FROM reports
        ORDER BY created_ts;
        """,
    )
    report_data = []
    for row in res:
        d = {
            "id": row[0],
            "created_ts": row[1],
            "fullname": row[2],
            "description": row[3],
            "severity": row[4],
        }
        report_data.append(d)

    con.close()

    # Render the template
    return flask.render_template(
        "report_list.html",  # Name of template file
        report_data=report_data,
    )


# MAIN PROGRAM

# Make sure database exists
add_sample_data = False
if not os.path.exists(DB_FILE):
    print("The database '{}' was not found.  Creating it.".format(DB_FILE))
    add_sample_data = True

con = sqlite3.connect(DB_FILE)

print("Making sure the DB contains the necessary tables...", end="")
con.execute(
    """
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY,
    created_ts REAL,
    fullname TEXT,
    description TEXT,
    severity TEXT
);
"""
)
print("Done")

if add_sample_data:
    print("Populating DB with sample data, since it was empty...", end="")
    con.execute(
        "INSERT INTO reports (fullname,description,severity,created_ts) VALUES (?,?,?,?)",
        (
            "Emily Dumas",
            "TrackFlow and OrderNova use 100% CPU for no apparent reason",
            "critical",
            time.time(),
        ),
    )
    print("Done")

con.commit()
con.close()

# Run the application
app.run()  # This will never return.  You lose all control over the program.
