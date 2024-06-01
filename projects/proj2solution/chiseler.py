# MCS 275 Spring 2023 Project 2 Solution
# Emily Dumas
"""
Module that finds winning strategies for the game 'word chiseler' where a list
of words is provided, and the player can choose to remove the first word or the
last word. If at any time the first and last words do not share any letters, the
game is lost. If the word list becomes empty, the game is won.
"""


def share_letter(w1, w2):
    "Determine whether there is a character common to strings `w1` and `w2`"
    for c in w1:
        if c in w2:
            return True
    return False


def winning_strategy(L, moves_so_far=None):
    """
    Find a winning strategy to the word chiseler game where the current state
    is `L` and `moves_so_far` contains the list of words removed thus far.
    """
    if moves_so_far == None:
        moves_so_far = []

    # One-word game always winnable
    if len(L) == 1:
        return moves_so_far + [L[0]]

    if not share_letter(L[0], L[-1]):
        # No shared letter = dead end, backtrack
        return None

    # Shared letter = two possible moves to try
    # (but return as soon as we find a single winner)

    # 1. Remove first word
    strat = winning_strategy(L[1:], moves_so_far + [L[0]])
    if strat:
        return strat
    # 2. Remove last word
    strat = winning_strategy(L[:-1], moves_so_far + [L[-1]])
    if strat:
        return strat

    # Neither move leads to a win
    return None


def all_winning_strategies(L, moves_so_far=None):
    """
    Find a winning strategy to the word chiseler game where the current state
    is `L` and `moves_so_far` contains the list of words removed thus far.
    """

    if moves_so_far == None:
        moves_so_far = []

    # Exactly one winning strategy for a one-word game
    # consisting of the moves so far, followed by removal
    # of that last word.
    if len(L) == 1:
        return [moves_so_far + [L[0]]]

    if not share_letter(L[0], L[-1]):
        # No shared letter = this game has no winning strategies
        return []

    # Two next moves are possible, so find:
    # 1. Strategies where the next move is to remove first word
    strats_first = all_winning_strategies(L[1:], moves_so_far + [L[0]])
    # 2. Strategies where the next move is to remove last word
    strats_last = all_winning_strategies(L[:-1], moves_so_far + [L[-1]])
    # Return all the strategies found.
    return strats_first + strats_last


def num_winning_strategies(L):
    "Total number of ways to win word chiseler with word list `L`"
    return len(all_winning_strategies(L))


def show_solved_game(sentence):
    """
    Given a `sentence` with distinct words, split and convert to upper case and
    show a way to win word chiseler for that list.
    """
    L = sentence.upper().split()
    S = winning_strategy(L)
    if S == None:
        raise Exception("This game has no winning strategy: " + " ".join(L))
    for move in S:
        print(" ".join(L))
        print("Remove:", move)
        if move == L[0]:
            L = L[1:]
        else:
            L = L[:-1]
