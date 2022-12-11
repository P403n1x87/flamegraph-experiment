from random import randint as r

from flamegraph import AustinFlameGraph, compare


def n():
    return r(-10, 10)


x = [
    AustinFlameGraph({"a": 100000 + n(), "b": 200000 + n(), "c": 300000 + n()})
    for _ in range(100)
]

y = [
    AustinFlameGraph({"a": 100000 + n(), "b": 400000 + n(), "c": 300000 + n()})
    for _ in range(100)
]

print(compare(x, y))
