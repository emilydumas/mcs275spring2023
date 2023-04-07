CREATE TABLE orders (
    woid INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    assigned_user TEXT,
    created_ts REAL NOT NULL,
    assigned_ts REAL,
    completed_ts REAL,
    CHECK (
        (assigned_ts IS NULL AND assigned_user IS NULL)
        OR
        (assigned_ts IS NOT NULL AND assigned_user IS NOT NULL)
    )
);