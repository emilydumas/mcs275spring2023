# MCS 275 Spring 2023 Project 1 Starter Pack
"Basic simulation to test shuttle autopilot"

# YOU ARE MEANT TO MODIFY THIS TO SUIT YOUR TESTING NEEDS!
# As provided it is a simulation of a shuttle that does
# nothing, because the starter pack only provides a
# `Shuttle` base class (which does nothing.)

import shuttle
import fixtures
import tui

# Make the supply cache, capacity 900
# (you can change the capacity if you like)
sc = fixtures.SupplyCache(900)

# Make the destination cache, capacity 500
# (you can change the capacity if you like)
dc = fixtures.DestinationCache(500)

# Make the shuttle autopilot for a shuttle with
# capacity 200 (change if you like).
S = shuttle.Shuttle(200, sc, dc)
# You might consider removing the previous line and replacing
# it with one of these, if you've written the corresponding
# subclass:
# S = shuttle.BackForthShuttle(200, sc, dc)
# S = shuttle.ActOnOverflowShuttle(200, sc, dc)
# S = shuttle.ActOnUnderflowShuttle(200, sc, dc)
# It's definitely a good idea to try different capacities.

# Fill the supply with sand (it starts empty by default!)
sc.stored = sc.capacity

# Clear terminal (scroll up 60 lines)
print("\n" * 60)

t = 0  # Tracks simulation time

# Main simulation loop runs forever
# (control-C or option-. to quit)
while True:
    print("State at time t={}:".format(t))
    tui.show(sc, dc, S)  # Display current situation
    print("\n" * 3)
    input("Press Enter to advance simulation")
    print("\n" * 60)
    S.update()
    # If you were going to add material at supply
    # or remove material from dest, that would go 
    # here.  Examples:
    # Add 50kg (per minute) to the supply
    #   sc.stored = min(sc.capacity,sc.stored+50)
    # Remove 10kg (per minute) from the destination
    #   dc.stored = max(0,dc.stored-10)
    # You could also add material only for certain
    # values of `t` to simulate sporadic arrivals.
    t += 1
