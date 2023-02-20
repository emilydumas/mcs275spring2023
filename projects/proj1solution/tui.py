# MCS 275 Spring 2023 Project 1 Starter Pack
"Make text-based graphics of the monorail track"

# YOU DO NOT NEED TO READ OR UNDERSTAND ANYTHING IN THIS FILE

trackstr = "          /---> |==========================| <---\          "
line1 = "  Supply cache                                  Dest cache  "
blank = " " * len(trackstr)


def trackpos(i):
    "Convert logical track position to character index"
    return 16 + 3 * i


def strdraw(s, t, pos):
    "Paste string `t` into string `s` starting at position `pos`"
    L = list(s)
    L[pos : pos + len(t)] = t
    return "".join(L)


def cache_desc(cache, x, width, align):
    "Return a list of strings describing the cache `cache` at position `x`"
    L = []
    L.append("{}kg held".format(cache.stored))
    L.append("{}kg max".format(cache.capacity))
    L.append("at x={}".format(x))
    if align == "left":
        L = [s[:width] + " " * (width - min(width, len(s))) for s in L]
    elif align == "right":
        L = [" " * (width - min(width, len(s))) + s[:width] for s in L]
    return L


def shuttle_desc(sh, width, align):
    "Return a list of strings describing the shuttle `sh`."
    L = []
    L.append("Shuttle")
    L.append("{}kg held".format(sh.stored))
    L.append("{}kg max".format(sh.capacity))
    L.append("at x={}".format(sh.pos))
    if hasattr(sh, "state"):
        L.append(str(sh.state))
    if align == "left":
        L = [s[:width] + " " * (width - min(width, len(s))) for s in L]
    elif align == "right":
        L = [" " * (width - min(width, len(s))) + s[:width] for s in L]
    elif align == "center":
        L = [s.center(width) for s in L]
    return L


def show(supply, dest, shuttle):
    """
    Take:
      `SupplyCache` object `supply`,
      `DestinationCache` object `dest`, and
      `Shuttle` object `shuttle`
    and display a text graphics representation of their state on the terminal.
    """
    lines = [strdraw(trackstr, "X", trackpos(shuttle.pos)), line1] + [
        str(blank) for _ in range(4)
    ]
    supdesc = cache_desc(supply, 0, 13, "right")
    for i, s in enumerate(supdesc):
        lines[i + 2] = strdraw(lines[i + 2], s, 0)
    destdesc = cache_desc(dest, 9, 12, "left")
    for i, s in enumerate(destdesc):
        lines[i + 2] = strdraw(lines[i + 2], s, trackpos(9) + 5)
    shutdesc = shuttle_desc(shuttle, 12, "center")
    k = trackpos(shuttle.pos) - 5
    if k < trackpos(0) - 2:
        k = trackpos(0) - 2
    if k + 12 > trackpos(9) + 3:
        k = (trackpos(9) + 3) - 12
    for i, s in enumerate(shutdesc):
        lines[i + 1] = strdraw(lines[i + 1], s, k)
    print("\n".join(lines))
