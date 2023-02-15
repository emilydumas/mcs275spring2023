# MCS 275 Spring 2023 Lectures 13 and 14
"Recursive comparison sorting algorithms"


def partition(L, start, end, verbose=False):
    """
    Partition L[start:end] using the
    last element (L[end-1]) as the pivot.
    Returns the position of the pivot.
    """
    pivot = L[end - 1]
    dst = start
    for src in range(start, end):  # challenge Q: Why can't we use range(start,end-1)
        if L[src] < pivot:
            # swap L[src], L[dst]
            L[src], L[dst] = L[dst], L[src]
            dst += 1

    # put the pivot into its final place
    L[end - 1], L[dst] = L[dst], L[end - 1]
    if verbose:
        print("Partitioned into:", L[start:dst], " ", L[dst], " ", L[dst + 1 : end])
    return dst


def quicksort(L, start=0, end=None, verbose=False):
    """
    Sort L[start:end] in place using
    quicksort.  Modifies L, returns nothing.
    """
    if end == None:
        # default to end of L
        end = len(L)
    # Are we done yet?!
    if end - start <= 1:
        return
    # Not done yet, need to partition L
    m = partition(L, start, end, verbose)
    # m is now the pivot position
    quicksort(L, start, m, verbose)  # orange (less than pivot)
    quicksort(L, m + 1, end, verbose)  # purple (>= pivot)


def merge(L0, L1, verbose=False):
    """
    Merge sorted lists `L0` and `L1`
    into a new sorted list and return it
    """
    L = []
    i0 = 0
    i1 = 0
    while i0 < len(L0) and i1 < len(L1):
        if L0[i0] <= L1[i1]:
            # Take from L0
            if verbose:
                print("Took {} from L0".format(L0[i0]))
            L.append(L0[i0])
            i0 += 1
        else:
            # Take from L1
            if verbose:
                print("Took {} from L1".format(L1[i1]))
            L.append(L1[i1])
            i1 += 1
    # Now one of the lists has been completely
    # used up.  But items may remain in the other
    while i0 < len(L0):
        if verbose:
            print("Copying over unused element {} from L0".format(L0[i0]))
        L.append(L0[i0])
        i0 += 1
    while i1 < len(L1):
        if verbose:
            print("Copying over unused element {} from L1".format(L1[i1]))
        L.append(L1[i1])
        i1 += 1
    return L


def mergesort(L, verbose=False):
    """
    Return a list with the same items
    as `L` but in increasing order.
    Uses the mergesort algorithm.
    """
    if verbose:
        print("Working on", L)
    if len(L) <= 1:
        if verbose:
            print("Already sorted.")
        return L

    # split and solve subproblems
    n = len(L)
    L0 = mergesort(L[: n // 2], verbose)
    L1 = mergesort(L[n // 2 :], verbose)

    if verbose:
        print("Merging", L0, "+", L1)

    # merge
    res = merge(L0, L1)
    if verbose:
        print("Returning", res)
    return res


if __name__ == "__main__":
    import random

    num_random_tests = 50_000

    print("*************")
    print("* MERGESORT *")
    print("*************")
    L = [8, 6, 4, 3, 5, 7, 1, 2]
    print("\nVerbose test with input", L, "\n--BEGIN FUNCTION CALL--")
    S = mergesort(L, verbose=True)
    print("--END FUNCTION CALL--\nReturn value", S)

    print("\nTesting mergesort on", num_random_tests, "permutations of range(0,100):")
    orig = list(range(100))
    for _ in range(num_random_tests):
        L = list(orig)  # make a copy of `orig`
        random.shuffle(L)
        assert orig == mergesort(L)
    print("PASS - All tested permutations correctly sorted.")

    print("\n" * 2)

    print("*************")
    print("* QUICKSORT *")
    print("*************")
    L = [7, 6, 2, 3, 5, 8, 1, 4]
    print("\nVerbose test with input", L, "\n--BEGIN FUNCTION CALL--")
    quicksort(L, verbose=True)
    print("--END FUNCTION CALL--\nAfter quicksort, list contains", S)

    print("\nTesting quicksort on", num_random_tests, "permutations of range(0,100):")
    orig = list(range(100))
    for _ in range(num_random_tests):
        L = list(orig)  # make a copy of `orig`
        random.shuffle(L)
        quicksort(L)
        assert orig == L
    print("PASS - All tested permutations correctly sorted.")
