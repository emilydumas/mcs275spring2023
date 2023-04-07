CREATE TABLE orders (
    woid INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    assigned_user TEXT,
    created_ts REAL NOT NULL,
    assigned_ts REAL,
    completed_ts REAL,
    CHECK (
        (assigned_user IS NULL AND assigned_ts IS NULL) OR
        (assigned_user IT NOT NULL AND asssigned_ts IS NOT NULL)
    )
);
