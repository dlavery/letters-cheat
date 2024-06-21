#!/usr/bin/python3
from itertools import combinations

def get_combinations(str, sample_size):
    ret = []
    s = sorted(str)
    for c in combinations(s, sample_size):
        ret.append(''.join(c))
    return ret

if __name__ == '__main__':
    c = get_combinations("WXYZABCDE", 8)
    print("combinations:")
    print("no of combinations:", len(c))
    ctr = 0
    for el in c:
        ctr += 1
        print("%2s: %s" % (ctr, el))
    print("you're done!")