# MCS 275 Spring 2023 Lectures 9 and 10
"Recursive functions and comparison iterative implementations"

# 0! = 1
# 1! = 1
# 2! = 2 * 1! = 2
# 3! = 3 * 2! = 6


def fact(n, verbose=False):
    "The factorial of a nonnegative integer `n` by an efficient recursive algorithm"
    if n < 0:
        raise ValueError("Only defined for n>=0")

    if verbose:
        print("fact({}) called".format(n))
    if n <= 1:
        return 1  # 0! = 1 and 1! = 1

    return n * fact(n - 1, verbose)


def fact_iterative(n):
    "The factorial of a nonnegative integer `n` computed with iteration"
    if n < 0:
        raise ValueError("Only defined for n>=0")
    prod = 1
    for i in range(2, n + 1):  # i starts at 2 and ends at n
        prod *= i

    return prod


# fib(0) = 0
# fib(1) = 1
#              ---->  fib(n)=n if n<=1
def fib(n, verbose=False):
    "The n^th fibonacci number computed by a ridiculously inefficient recursive algorithm"
    if n < 0:
        raise ValueError(
            "This implementation of Fibonacci sequence only calculates F_n for n>=0"
        )

    if verbose:
        print("fib({}) called".format(n))

    if n <= 1:
        return n  # handles fib(0)=0 and fib(1)=1

    return fib(n - 1, verbose) + fib(n - 2, verbose)


# Cache dictionary, maps key n to value fib(n)
# Initially contains keys 0,1 which act as
# base cases for the recursion in fib_memoized.
fib_cache = {
    0: 0,
    1: 1,
}


def fib_memoized(n):
    "The n^th fibonacci number computed by a ridiculously inefficient recursive algorithm"
    if n < 0:
        raise ValueError(
            "This implementation of Fibonacci sequence only calculates F_n for n>=0"
        )

    if n in fib_cache:
        return fib_cache[n]

    result = fib_memoized(n - 1) + fib_memoized(n - 2)
    fib_cache[n] = result  # store for later use!
    return result


def fib_memoized_clear_cache():
    "Forget all cached values of fib_memoized"
    fib_cache.clear()
    fib_cache[0] = 0
    fib_cache[1] = 1


def fib_iterative(n):
    "The n^th fibonacci number computed by an iterative algorithm"
    # initialize state  - solution to a small sub-problem
    if n <= 1:
        return n
    a = 0  # fib(0)
    b = 1  # fib(1)
    # loop - solve successively larger sub-problems, updating state
    for _ in range(n - 1):
        a, b = b, a + b  # replace fib(k) and fib(k+1) with fib(k+1) and fib(k+2)
        # NOTE: Previous line could be replaced with these three:
        #   new_b = a+b
        #   a = b
        #   b = new_b

    return b


# a,b = b,a is Python for swap

# Suppose n = 4
# Initially a=0=fib(0) b=1=fib(1)
# After one iteration of loop
# a=1=fib(1) and b=1=fib(2)
# After two iterations of loop
# a=1=fib(2) and b=3=fib(3)
# After three iterations of loop
# a=3=fib(3) and b=5=fib(4)


def pfs(n):
    """
    The n^th paper folding sequence, describing the ridge directions
    of a strip of paper folded n times and then unfolded, as binary
    digits (1 = upward crease, 0 = downward crease).  Returns a list
    of integers.
    """
    if n < 0:
        raise ValueError("Only defined for n>=0")

    if n == 0:
        return []

    # Reminder: list addition in Python is concatenation
    # e.g. [1,2,3] + [4,5,6] = [1,2,3,4,5,6]
    prev = pfs(n - 1)
    # return prev, then 1, then prev in reverse order and flipped
    return prev + [1] + [1 - x for x in prev[::-1]]


def pfs_iterative(n):
    """
    The n^th paper folding sequence, iteratively
    """
    if n < 0:
        raise ValueError("Only defined for n>=0")

    L = []  # Initially no creases

    for _ in range(n):
        L = L + [1] + [1 - x for x in L[::-1]]  # fold!
    return L
