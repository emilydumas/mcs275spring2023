-- show column headings
.headers on
-- pretty tables
.mode box

-- Show what tables exist
.tables

-- Describe the powerplants table
.schema powerplants

-- How many rows are present
SELECT COUNT(*) FROM powerplants;

-- Power plants with a capacity of at least 8GW
SELECT country,name,capacity_mw
FROM powerplants
WHERE capacity_mw > 8000;

-- 10 largest nuclear power plants
SELECT gppd_id,country,name,capacity_mw
FROM powerplants
WHERE primary_fuel = "Nuclear"
ORDER BY capacity_mw DESC
LIMIT 10;

-- Fuels that are present
SELECT DISTINCT primary_fuel
FROM powerplants;

-- Fuel combinations that are present
SELECT DISTINCT primary_fuel, secondary_fuel
FROM powerplants;

-- Number of coal plants in Russia
SELECT COUNT(*)
FROM powerplants
WHERE 
    country="Russia" AND
    primary_fuel="Coal";

-- Number of coal plants in Russia that also have a secondary fuel
SELECT COUNT(*)
FROM powerplants
WHERE 
    country="Russia" AND
    primary_fuel="Coal" AND
    secondary_fuel IS NOT NULL;

-- Top 10 gas plants by utilization (output/capacity) in 2016
SELECT country,name,output_gwh_2016/capacity_mw
FROM powerplants
WHERE
    output_gwh_2016 IS NOT NULL AND
    primary_fuel="Gas"
ORDER BY output_gwh_2016/capacity_mw DESC
LIMIT 10;

-- Same as last query but using custom column naming
SELECT country,name,output_gwh_2016/capacity_mw as util_ratio
FROM powerplants
WHERE
    output_gwh_2016 IS NOT NULL AND
    primary_fuel="Gas"
ORDER BY util_ratio DESC
LIMIT 10;

-- Countries that contain a hydroelectric plant of at least 2GW
SELECT DISTINCT country
FROM powerplants
WHERE
    primary_fuel="Hydro" AND
    capacity_mw>2000;
