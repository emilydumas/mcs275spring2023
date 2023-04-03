# Plans for ORDERNOVA
The 12pm section application

## Views
* Submitter view: Create a new work order (form)
* Worker view: List, allow to take on assignment or complete one already assigned
* Admin view: Like worker view but with additional functions not specific to any one worker

## Worker view

Probably the most complicated view in the application.  (Read in CRUD, with buttons for Update as well.)

Knows the id number of the worker for which it is showing information.

Two lists:
* A list of work orders that have already been assigned to this worker id
    * Button to mark WO complete
    * Button to unassign this WO
* A list of worker orders not yet assigned to anyone
    * Button to accept this WO as an assignment

Dates?  (Oh but how to do that in Python...)
