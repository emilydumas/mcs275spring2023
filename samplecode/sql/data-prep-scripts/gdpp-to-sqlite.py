"Download the Global Power Plant Database and convert from CSV to sqlite3"
# MCS 275 Spring 2023
# Emily Dumas
import urllib.request
import os
import csv
import zipfile
from io import TextIOWrapper
import sqlite3

gdpp_url = "https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip"
gdpp_file = "global_power_plant_database_v_1_3.zip"
gdpp_sqlite = "powerplants.sqlite"

if not os.path.exists(gdpp_file):
    print("Downloading {}".format(gdpp_url))
    with urllib.request.urlopen(gdpp_url) as response:
        data = response.read()
    with open(gdpp_file,"wb") as fp:
        fp.write(data)

con = sqlite3.connect(gdpp_sqlite)
con.execute("DROP TABLE IF EXISTS powerplants;")
con.execute("""
CREATE TABLE powerplants (
    id INTEGER PRIMARY KEY,
    gppd_id TEXT,
    country TEXT,
    name TEXT,
    capacity_mw REAL,
    latitude REAL,
    longitude REAL,
    primary_fuel TEXT,
    secondary_fuel TEXT,
    year_commissioned INTEGER,
    owner TEXT,
    output_gwh_2013 REAL,
    output_gwh_2014 REAL,
    output_gwh_2015 REAL,
    output_gwh_2016 REAL,
    output_gwh_2017 REAL,
    output_gwh_2018 REAL,
    output_gwh_2019 REAL
);
""")

# Mappings from input field names to output field names

text_fields = {
    "gppd_idnr": "gppd_id",
    "country_long": "country",
    "name": "name",
    "primary_fuel": "primary_fuel",
    "other_fuel1": "secondary_fuel",
    "owner": "owner",
}

integer_fields = {
    "commissioning_year": "year_commissioned",
}

real_fields = {
    "capacity_mw": "capacity_mw",
    "latitude": "latitude",
    "longitude": "longitude",
    "generation_gwh_2013": "output_gwh_2013",
    "generation_gwh_2014": "output_gwh_2014",
    "generation_gwh_2015": "output_gwh_2015",
    "generation_gwh_2016": "output_gwh_2016",
    "generation_gwh_2017": "output_gwh_2017",
    "generation_gwh_2018": "output_gwh_2018",
    "generation_gwh_2019": "output_gwh_2019",
}

with zipfile.ZipFile(gdpp_file, mode="r") as archive:
    csvs = []
    for info in archive.infolist():
        if info.filename.endswith(".csv"):
            csvs.append(info)

    if not csvs:
        print("{} does not contain any CSV files".format(gdpp_file))
        exit(1)

    m = max(csvs,key=lambda info:info.file_size)
    print("Archive contains {} CSV files, largest of size {} named '{}'".format(len(csvs),m.file_size,m.filename))

    reader = csv.DictReader(TextIOWrapper(archive.open(m.filename,"r"),"UTF-8"))
    N = 0
    for row in reader:
        outrow = dict()
        for inf,outf in text_fields.items():
            outrow[outf] = row[inf] if row[inf] else None
        for inf,outf in integer_fields.items():
            x = float(row[inf]) if row[inf] else None
            if x is not None:
                x = int(x)
            outrow[outf] = x  
        for inf,outf in real_fields.items():
            outrow[outf] = float(row[inf]) if row[inf] else None
        cols = list(outrow.keys())
        colstr = ", ".join(cols)
        phstr = ("?,"*len(cols))[:-1]
        con.execute(
            "INSERT INTO powerplants ("+colstr+") VALUES ("+phstr+");",
            [ outrow[c] for c in cols ]
        )
        N += 1

con.commit()
print("Added {} rows to table 'powerplants'.".format(N))
con.close()