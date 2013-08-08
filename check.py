#! /usr/bin/env python3

import json
import io

def determineCollision(classTime):
    d = dict()
    for m in classTime:
        d[m] = [];
        rem = classTime.copy();
        s = set(classTime[m])
        del rem[m]
        for m2 in rem:
            if not s.isdisjoint( rem[m2] ):
                d[m] += [m2]
    return d

def findSame(dispo):
    d = dict()
    for c in dispo:
        pref = c[0:7]
        if pref not in d:
            d[pref] = []
        if '-' in c:
            d[pref] += [c]
        else:
            del d[pref]

    c = dict()
    for k in d:
        for ek in d[k]:
            c[ek] = set(d[k]) - {ek}

    return c

def mergeConflict(*con):
    d = con[0].copy()
    for c in con[1:]:
        for k in c:
            if k in d:
                d[k] += c[k]
            else:
                d[k] = c[k]
    return d

def chooseClass(number, dispo, conflict):
    if number == 0:
        yield []
    else:
        for d in dispo:
            for other in chooseClass(number-1,dispo - {d} - set(conflict[d]),conflict):
                yield [d] + other

def main():
    j = json.load(open("class.json"))
    t = j["time"]
    print("------- T ------")
    #print(t)
    d = determineCollision(t)
    print("------- D ------")
    print(d)
    c = findSame(set(t.keys()))
    print("------- C ------")
    print(c)
    m = mergeConflict(d,c)
    print("------- M ------")
    print(m)

    h = list(chooseClass(3,set(t.keys()) - set(j["taken"]),d))
    print("Possibility:")
    print(len(h))
    print("Example:")
    print(h[0:5])

if __name__ == '__main__':
    main()
