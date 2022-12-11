import os
from time import sleep


def a():
    sleep(0.15 if os.getenv("REGRESSION", False) else 0.2)


def b():
    a()
    sleep(0.1)


def c():
    b()
    sleep(0.05)


c()
