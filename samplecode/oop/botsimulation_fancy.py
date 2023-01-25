"""Robot motion simulation with unicode text graphics"""
# MCS 275 Spring 2023 David Dumas

from plane import Vector2, Point2
import bots
import random

width = 60
height = 30

current_bots = []
for i in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.Bot(position=P))

n = 0
while True:
    print("\n" * 3 * height)
    board = [[" "] * width for _ in range(height)]
    for b in current_bots:
        if b.position.x < 0 or b.position.x >= width:
            continue
        elif b.position.y < 0 or b.position.y >= height:
            continue
        if b.active:
            if hasattr(b, "symbol"):
                mark = b.symbol
            else:
                mark = "*"
            board[b.position.y][b.position.x] = mark
        else:
            board[b.position.y][b.position.x] = "\u2620"
    for row in board:
        print("".join(row))
    print("time={}".format(n))
    input()

    for b in current_bots:
        b.update()
    n += 1
