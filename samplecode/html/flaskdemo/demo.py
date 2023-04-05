# MCS 275 Spring 2023 Lecture 31
"Simple Flask demo"

# To try it, run the script and then try loading in a browser:
# http://localhost:5000/onions/
# http://localhost:5000/static/walrus.html
# http://localhost:5000/static/kitten.jpg  (for an AI-generated drawing of a cute kitten)
# http://localhost:5000/ordernova/workerview/ (ordernova worker view template)
# http://localhost:5000/trackflow/workerview/ (trackflow worker view template)

# Or you might need to replace 5000 with whatever port number Flask decides to use.
# It shows the one it uses in the startup message.

import flask
import random

# Create Flask (application) object
app = flask.Flask("MCS 275 demo application")

# Define routes (functions that determine what URLs
# the application will respond to)

# --------------------------------------------------------
# 1. Example of how to return a fixed string with HTML
# and make it the result of visiting a certain URL


@app.route("/onions/")  # URL http://localhost:8000/onions/ is route "/onions/"
def function_name_user_will_never_see():
    return """<!doctype html>
<html>
<head><title>Hello world</title></head>
<body>
<p>This HTML document was returned by a function called in my Flask application.</p>
<p>All I had to do was write the function and tell Flask about it.</p>
</body>
</html>
"""


# --------------------------------------------------------
# 2. Example of how to return a file from disk

# !! Nothing needs to appear in the program to do this !!
# Just put the file (e.g. kitten.jpg) in the static/ subdirectory and
# flask will serve it under route "/static/kitten.jpg")


# --------------------------------------------------------
# 3. Example of how to render a HTML template, filling in
# values for the placeholders therein


@app.route("/ordernova/workerview/")
def render_on_workerview():
    "Render a simple template with random values"
    # Note: the usernames, descriptions, and dates are chosen independently
    # and are not representative of any real events.
    user = random.choice(["alincoln", "bobama", "gwashington", "ljohnson"])
    desc = random.choice(
        [
            "Choose treasury secretary",
            "Bring umbrella to work",
            "Renovate oval office",
            "Work on golf game",
        ]
    )
    woid = random.randint(1, 50)
    datestr = random.choice(
        [
            "12 Jan 1777",
            "3 Mar 2008",
            "11 Jun 1966",
            "21 November 1864",
        ]
    )
    return flask.render_template(
        "on-workerview.html",  # Name of template file
        username=user,  # name=value to use in filling template
        description=desc,  # name=value to use in filling template
        woid=woid,  # ...
        datestr=datestr,
    )


@app.route("/trackflow/workerview/")
def render_tf_workerview():
    "Render a simple template with random values"
    # Note: the usernames, descriptions, and dates are chosen independently
    # and are not representative of any real events.
    user = random.choice(["htaft", "wclinton", "jcarter", "jkennedy"])
    desc = random.choice(
        [
            "Complete WH bathroom renovation",
            "Upgrade from dial-up to ISDN",
            "Sell peanut farm",
            "Investigate moon mission feasibility",
        ]
    )
    woid = random.randint(1, 50)
    datestr = random.choice(
        [
            "1 Jan 1900",
            "17 Apr 1998",
            "4 Sep 1977",
            "5 Dec 1961",
        ]
    )
    return flask.render_template(
        "tf-workerview.html",  # Name of template file
        username=user,  # name=value to use in filling template
        description=desc,  # name=value to use in filling template
        woid=woid,  # ...
        datestr=datestr,
    )


# Run the application
app.run()  # This will never return.  You lose all control over the program.
