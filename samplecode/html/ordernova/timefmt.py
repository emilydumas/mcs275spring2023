"Functions for giving human-readable datetimes and intervals"
import datetime

def ts_fmt(x):
    "Format a timestamp `x` as a nice string"
    return datetime.datetime.fromtimestamp(x).strftime("%-I:%M%p on %B %d, %Y")


def tsdiff_fmt(t):
    """
    Describe something `t` seconds in the past in approximate and
    human-friendly units
    """
    if t < 0:
        return "in the future"
    if t < 5:
        return "now"
    if t < 55:
        return "{} seconds ago".format(int(t))
    m = t / 60
    if m < 60:
        im = int(m)
        if im > 1:
            suffix = "s"
        else:
            suffix = ""
        return "{} minute{} ago".format(im, suffix)
    h = m / 60
    if h < 24:
        ih = int(h)
        if ih > 1:
            suffix = "s"
        else:
            suffix = ""
        return "{} hour{} ago".format(ih, suffix)
    d = int(h / 24)
    if d > 1:
        suffix = "s"
    else:
        suffix = ""
    return "{} day{} ago".format(d, suffix)
