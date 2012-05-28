# vim: sts=4 ts=8 et ai

import string

def qsort(lst, func=None):
    if len(lst) <= 1:
        return lst
    if func == None:
        func = type(lst[0]).__lt__
    pivot = lst.pop(0)
    greater_eq = qsort([i for i in lst if not func(i, pivot)], func)
    lesser = qsort([i for i in lst if func(i, pivot)], func)
    return lesser + [pivot] + greater_eq

def _unique(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield x

def unique(seq):
    return list(_unique(seq))

def list_clear(seq):
    """Removes empty elements from list"""
    res = list(seq)
    i = 0
    while i < len(res):
        if not res[i]:
            del res[i]
            i -= 1
        i += 1
    return res

# from git's levenhstein.c:
#
# This function implements the Damerau-Levenshtein algorithm to
# calculate a distance between strings.
#
# Basically, it says how many letters need to be swapped, substituted,
# deleted from, or added to string1, at least, to get string2.
#
# The idea is to build a distance matrix for the substrings of both
# strings.  To avoid a large space complexity, only the last three rows
# are kept in memory (if swaps had the same or higher cost as one deletion
# plus one insertion, only two rows would be needed).
#
# At any stage, "i + 1" denotes the length of the current substring of
# string1 that the distance is calculated for.
#
# row2 holds the current row, row1 the previous row (i.e. for the substring
# of string1 of length "i"), and row0 the row before that.
#
# In other words, at the start of the big loop, row2[j + 1] contains the
# Damerau-Levenshtein distance between the substring of string1 of length
# "i" and the substring of string2 of length "j + 1".
#
# All the big loop does is determine the partial minimum-cost paths.
#
# It does so by calculating the costs of the path ending in characters
# i (in string1) and j (in string2), respectively, given that the last
# operation is a substition, a swap, a deletion, or an insertion.
#
# This implementation allows the costs to be weighted:
#
# - w (as in "sWap")
# - s (as in "Substitution")
# - a (for insertion, AKA "Add")
# - d (as in "Deletion")
#
# Note that this algorithm calculates a distance _iff_ d == a.
#
def levenhstein(str1, str2, w, a, s, d):
    len1 = len(str1)
    len2 = len(str2)
    l = len1
    row0=[0] * (len2 + 1)
    row1=[0] * (len2 + 1)
    row2=[0] * (len2 + 1)

    if len2 > l:
        l = len2

    for i in range(0,len2 + 1):
          row1[i] = i * a

    for i in range(0, len1):
        row2[0] = (i + 1) * d

        for j in range(0, len2):
            # subst
            if (str1[i] != str2[j]):
                    row2[j + 1] = row1[j] + s
            else:
                    row2[j + 1] = row1[j]
            # swap
            if (i > 0 and j > 0 and str1[i - 1] == str2[j] and  \
                        str1[i] == str2[j - 1] and \
                        row2[j + 1] > row0[j - 1] + w):
                  row2[j + 1] = row0[j -1] + w
            # deletion
            if row2[j + 1] > row1[j + 1 ] + d:
                    row2[j+1] = row1[j + 1] + d
            # insertion
            if row2[j + 1] > row2[j] + a:
                    row2[j+1] = row2[j] + a

        dummy = list(row0)
        row0 = row1
        row1 = row2
        row2 = dummy

    return row1[len2]
