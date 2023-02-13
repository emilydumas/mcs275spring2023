# MCS 275 Spring 2023 Lecture 13
"Recursive comparison sorting algorithms"


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
        print("mergesort called on", L)
    if len(L) <= 1:
        if verbose:
            print("returning", L, "as it is already sorted")
        return L

    # split and solve subproblems
    n = len(L)
    L0 = mergesort(L[: n // 2], verbose)
    L1 = mergesort(L[n // 2 :], verbose)

    if verbose:
        print("Recursive calls yielded sorted sublists", L0, "and", L1)

    # merge
    res = merge(L0, L1)
    if verbose:
        print("Merged to obtain", res)
    return res
