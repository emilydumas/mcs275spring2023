# MCS 275 Spring 2023 Lecture 9
"Recursive functions"

# 0! = 1
# 1! = 1
# 2! = 2 * 1! = 2
# 3! = 3 * 2! = 6

def fact(n,verbose=False):
    "The factorial of a nonnegative integer `n` by an efficient recursive algorithm"

    if verbose:
        print("fact({}) called".format(n))
    if n <= 1:
        return 1  # 0! = 1 and 1! = 1
    
    return n * fact(n-1,verbose)


# fib(0) = 0
# fib(1) = 1
#              ---->  fib(n)=n if n<=1
def fib(n,verbose=False):
    "The n^th fibonacci number computed by a ridiculously inefficient recursive algorithm"
    if verbose:
        print("fib({}) called".format(n))

    if n<=1:
        return n   # handles fib(0)=0 and fib(1)=1

    return fib(n-1,verbose) + fib(n-2,verbose)

def pfs(n):
    """
    The n^th paper folding sequence, describing the ridge directions
    of a strip of paper folded n times and then unfolded, as binary
    digits (1 = upward crease, 0 = downward crease).  Returns a list
    of integers.
    """
    if n == 1:
        return [1]
    
    # Reminder: list addition in Python is concatenation
    # e.g. [1,2,3] + [4,5,6] = [1,2,3,4,5,6]
    prev = pfs(n-1)
    #return prev, then 1, then prev in reverse order and flipped
    return prev + [1] + [ 1-x for x in prev[::-1] ]