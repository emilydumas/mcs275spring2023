# MCS 275 Spring 2023
"Simple Flask demo that returns an image"

import flask
import numpy as np
import PIL.Image
import io

# Create Flask (application) object
app = flask.Flask("MCS 275 image demo")

# Define routes (functions that determine what URLs
# the application will respond to)

# --------------------------------------------------------
# 1. Example of how to return a fixed string with HTML
# and make it the result of visiting a certain URL


@app.route("/")
def color_static_page():
    return """<!doctype html>
<html>
    <head>
    <title>Random color static</title>
    <style>
    body { max-width: 45rem; margin: auto; }
    </style>
    </head>
    <body>
    <h1>Random color static</h1>
    <p>Here is your custom random color static image, generated just for you in response to this request.
    It is probably different from every image ever seen by humans, and will not be seen again.
    (After you reload or close the page, this image is lost.)</p>
    <img src="/random-color-static.png">
    </body>
    </html>
"""


@app.route("/random-color-static.png")
def color_static_image():
    """
    Route that looks like the name of an image file but is
    actually a dynamically generated image.
    """
    # Make random data
    data = (np.random.random((512, 512, 3)) * 255).astype("uint8")
    # Convert to random colorful PIL image
    img = PIL.Image.fromarray(data)
    # PIL can write PNG or JPEG to a file, but not to memory
    # But Python has a class (StringIO) that lets you create a
    # fake file object where the data stays in memory.
    fake_output_file = io.BytesIO()
    # Have PIL write a PNG to that memory-backed fake file
    img.save(fake_output_file, "png")  # need to specify format in second arg
    fake_output_file.seek(0)  # Put file pointer back at start so we can read it back
    # Ask Flask to return the contents of our "file"
    return flask.send_file(fake_output_file, mimetype="image/png", max_age=0)
    # Omit max_age to allow this response to be cached!


app.run()
