import functools
import os
from os.path import join


opendbfile = functools.partial(
    open,
    join(os.environ['HOME'], '.local/share/todolist.csv')
)


def append(list_, item):
    with opendbfile('a+') as f:
        f.write(f'{list_},{item}\n')


def getall(*a, **k):
    with opendbfile(*a, **k) as f:
        for l in f:
            yield l.strip().split(',', 1)


def delete(list_, item):
    data = [(l, i) for l, i in getall() if l != list_ or i != item]
    with opendbfile('w') as f:
        for l, i in data:
            f.write(f'{l},{i}\n')

