"Simple SQLite-based todo list application"
# MCS 275 Spring 2023
# Emily Dumas
import os
import sys
import sqlite3


def usage(msg=None):
    "Display help and quit"
    if msg:
        print(msg)
    print(
        """
Usage:
    {0} add DESCRIPTION -- create new task
    {0} list -- show tasks not marked as done
    {0} listall -- show all tasks
    {0} done ID -- mark task with given id as done
    {0} undone ID -- mark task with given id as not done
    {0} delete ID -- delete task entirely
""".strip().format(
            sys.argv[0]
        )
    )
    exit(1)  # 1 means exit and tell OS it was an error


argc = len(sys.argv)

known_modes = ["add", "list", "listall", "done", "undo", "undone", "delete"]

if argc == 1:
    usage()

mode = sys.argv[1].lower()
if mode not in known_modes:
    usage("Unknown command '{}'".format(mode))

# This inscrutable line determines the dir containing the script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Now we compose a filename that looks for the DB
# in the same directory as the script.
db_filename = os.path.join(script_dir, "todo.sqlite")

# Open the database
con = sqlite3.connect(db_filename)

# Ensure the tasks table exists
with con:
    con.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        description TEXT,
        completed INTEGER DEFAULT 0
    );
    """
    )

if mode == "add":
    # Insert a task (INSERT query)
    desc = " ".join(sys.argv[2:])
    with con:
        con.execute("INSERT INTO tasks (description) VALUES (?);", [desc])
        res = con.execute("SELECT LAST_INSERT_ROWID();")
        newid = res.fetchone()[0]
    print("Added as task {}".format(newid))
elif mode in ["list", "listall"]:
    # List tasks (SELECT query)
    if mode == "list":
        query = "SELECT id,description,completed FROM tasks WHERE completed=0;"
    else:
        query = "SELECT id,description,completed FROM tasks;"
    res = con.execute(query)
    print("   ID DESCRIPTION")
    showed_a_task = False
    for row in res:
        showed_a_task = True
        disposition = " "
        if row[2]:
            disposition = "✓"
        print(
            "{} {:3d} {}".format(
                disposition,
                row[0],  # id
                row[1],  # description
            )
        )
    if not showed_a_task:
        print(" -- no tasks to show --")
    if mode == "list":
        res = con.execute("SELECT COUNT(*) FROM tasks WHERE completed=1;")
        notshown = res.fetchone()[0]
        if notshown:
            suffix = ""
            if notshown > 1:
                suffix = "s"
            print("({} completed task{} not shown)".format(notshown, suffix))
elif mode in ["done", "undo", "undone"]:
    # Mark a task as done / not done (UPDATE query)
    taskid = int(sys.argv[2])
    if mode == "done":
        c = 1
        status_desc = "done"
    else:
        c = 0
        status_desc = "not done"

    with con:
        con.execute("UPDATE tasks SET completed=? WHERE id=?;", (c, taskid))
        res = con.execute("SELECT CHANGES();")
        num_updated = res.fetchone()[0]
    if num_updated:
        print("Task {} marked as {}".format(taskid, status_desc))
    else:
        print("No task with id {} exists (no action taken)".format(taskid))
elif mode == "delete":
    # Remove a task (DELETE query)
    taskid = int(sys.argv[2])
    with con:
        con.execute("DELETE FROM tasks WHERE id=?;", (taskid,))
        res = con.execute("SELECT CHANGES();")
        num_deleted = res.fetchone()[0]
    if num_deleted:
        print("Task {} deleted".format(taskid))
    else:
        print("No task with id {} exists (no action taken)".format(taskid))
