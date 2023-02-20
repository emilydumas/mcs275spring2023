# MCS 275 Spring 2023 Project 1 Solution
"Basic simulation to test shuttle autopilot"

import shuttle
import fixtures
import tui
import time

# Make the supply cache, capacity 900
# (you can change the capacity if you like)
sc = fixtures.SupplyCache(900)

# Make the destination cache, capacity 500
# (you can change the capacity if you like)
dc = fixtures.DestinationCache(500)

# Make the shuttle autopilot for a shuttle with
# capacity 200 (change if you like).
S = shuttle.ActOnUnderflowShuttle(200, sc, dc)
# It's definitely a good idea to try different capacities.

# Fill the supply and dest with sand
sc.stored = sc.capacity
dc.stored = dc.capacity

# Clear terminal (scroll up 60 lines)
print("\n" * 60)

t = 0  # Tracks simulation time

# Main simulation loop runs forever
# (control-C or option-. to quit)
while True:
    print("State at time t={}:".format(t))
    tui.show(sc, dc, S)  # Display current situation
    print("\n" * 3)
    if t==0:
        time.sleep(2)
    else:
        time.sleep(0.3)
    print("\n" * 60)
    S.update()
    if t%30 == 0:
        sc.stored = min(sc.capacity,sc.stored+280)
    dc.stored = max(0,dc.stored-10)
    t += 1
