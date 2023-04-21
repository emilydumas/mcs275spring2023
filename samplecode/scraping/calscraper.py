"Download UIC academic calendar, write to CSV and JSON files"
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import csv
import time

url = "https://catalog.uic.edu/ucat/academic-calendar/"
out_csv = "calendar.csv"
out_json = "calendar.json"

print("Pausing 5 seconds to limit speed of requsts to uic.edu")
time.sleep(5)

print("Fetching '{}'".format(url))
with urlopen(url) as r:
    soup = BeautifulSoup(r, "html.parser")

print("Extracting data")
# The first three tables use a different format; drop them
# TODO: Make the recognition of different format automatic
good_tables = soup.find_all("table")[3:]


def is_term_heading(row):
    """
    Does this row of the table appear to introduce a new
    term and/or year (e.g. Fall Semester 2023)
    """
    first_td = row.td
    if first_td == None:
        return False
    s = first_td.text.lower()
    if "summer" in s or "fall" in s or "spring" in s:
        return True
    return False


year = None
term = None
schedule_events = []
for t in good_tables:
    for row in t.find_all("tr"):
        if is_term_heading(row):
            # Row looks like one of these
            #  Fall Semester 2023
            #  Summer Sessions 2023
            #  Summer Session 2 (8-Week)
            # We want the term and/or year to be extracted.
            s = row.text.lower()  # Full text of the row
            fields = s.split()  # all the words
            try:
                # See if the last word is a number.
                # If this works, then we're seeing something like "Fall Semester 2022"
                year = int(fields[-1])  # e.g. 2022
                term = fields[0].lower()  # e.g. "fall"
            except ValueError:
                # We're seeing something like "Summer Session 1 (4-Week)"
                # So we don't have a new year, but want to update the term
                if s.startswith("summer session 1"):
                    term = "summer1"
                elif s.startswith("summer session 2"):
                    term = "summer2"
                else:
                    raise ValueError("Don't know how to handle heading: '{}'".format(s))
        else:
            # We have a row that doesn't look like a term/year indicator
            # But it might still be the column headers (Date Event) rather
            # than an actual entry.
            heading = row.find("th")
            if heading != None:
                continue  # skip all rows that give column headings

            # Finally we're in the most common case: A row containing a calendar
            # event like
            #    December 8, F.  Instruction Ends."
            # Record this schedule item dictionary
            assert year != None  # We should have seen the year previously
            assert term != None  # We should have seen the term previously
            assert term != "summer"  # Subheading should make it "summer1" or "summer2"
            cells = row.find_all("td")
            schedule_events.append(
                {
                    "year": year,
                    "term": term,
                    "date": cells[0].text,  # content of the first td
                    "event": cells[1].text,  # context of the second td
                }
            )

print("Found {} events".format(len(schedule_events)))

print("Writing '{}'".format(out_csv))

with open(out_csv, "wt", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=["year", "term", "date", "event"])
    writer.writeheader()
    for d in schedule_events:
        writer.writerow(d)

print("Writing '{}'".format(out_json))
with open(out_json, "w") as fp:
    json.dump(schedule_events, fp)
