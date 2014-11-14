
import sys
from collections import defaultdict
from itertools import groupby
import os.path

def tohex(x):
    return int(x, 16)

def diff(hex1, hex2):
    i = tohex(hex1)
    j = tohex(hex2)
    return j - i == 1

def dup(x):
    return (x, x)

def fmt(x):
    return "\\x" + str(x)

def main():
    infile = "UnicodeData.txt"
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    elif os.path.isfile(infile):
        f = open(infile);
    else:
        from urllib.request import urlopen
        url = "http://www.unicode.org/Public/UNIDATA/UnicodeData.txt"
        f = map(lambda x: x.decode(), urlopen(url))


    lines = [ (lambda x: (x[2],x[0]))(line[:-1].split(';')) for line in f ]
    print(lines)
    lines.sort()
    l = groupby(lines, lambda x: x[0])
    d = defaultdict(list)
    for k,g in l:
        res = []
        lst = list(map(lambda x: x[1], g))
        lst.sort(key=tohex)
        n = len(lst)

        if n == 0:
            continue
        elif n == 1:
            res.append(map(fmt, dup(lst[0])))
        else:
            start = lst[0]
            current = start
            next = lst[1]
            for i in range(1, len(lst) - 1):
                if (not diff(current, next)):
                    end = next
                    res.append(map(fmt, (start, current)))
                    start = next
                else:
                    end = next

                current = lst[i]
                next = lst[i+1]
        out = ["["]
        for (x, y) in res:
            s = x
            if x != y:
                s += "-" + y
            out.append(s)
        out.append("]")
        d[k.lower()] = " ".join(out)
    keys = list(d.keys())
    keys.sort()
    for k,g in groupby(keys, lambda x: x[0]):
        lg = list(g)
        for kk in lg:
            print("$" + kk + " = " + d[kk])
        print("$" + k + " = [ " + " ".join(map(lambda x: "$" + x, lg)) + " ]")


if __name__ == '__main__':
    main()
