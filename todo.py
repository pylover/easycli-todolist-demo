import functools
from os.path import join, dirname

import easycli


__version__ = '0.1.0'


opendbfile = functools.partial(
    open,
    join(dirname(__file__), 'data.csv')
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


def listcompleter(prefix, action, parser, parsed_args):
    return set(l for l, _ in getall())


def itemcompleter(prefix, action, parser, parsed_args):
    list_ = parsed_args.list
    return list(i for l, i in getall() if l == list_)


ListArgument = functools.partial(
    easycli.Argument,
    'list',
    default='',
    help='List name',
    completer=listcompleter
)


ItemArgument = functools.partial(
    easycli.Argument,
    'item',
    help='Item name',
    completer=itemcompleter
)


class Delete(easycli.SubCommand):
    __command__ = 'delete'
    __aliases__ = ['d']
    __arguments__ = [
        ListArgument(),
        ItemArgument(),
    ]

    def __call__(self, args):
        delete(args.list, args.item)


class Show(easycli.SubCommand):
    __command__ = 'show'
    __aliases__ = ['s', 'l']
    __arguments__ = [
        ListArgument(nargs='?')
    ]

    def __call__(self, args):
        if args.list:
            for l, i in getall():
                if l == args.list:
                    print(i)

        else:
            for l, i in getall():
                print(f'{l}\t{i}')


class Append(easycli.SubCommand):
    __command__ = 'append'
    __aliases__ = ['add', 'a']
    __arguments__ = [
        ListArgument(),
        ItemArgument(),
    ]

    def __call__(self, args):
        append(args.list, args.item)


class Todo(easycli.Root):
    __help__ = 'Simple todo list'
    __completion__ = True
    __arguments__ = [
        easycli.Argument(
            '-v', '--version',
            action='store_true',
            help='Show version'
        ),
        Append,
        Show,
        Delete,
    ]

    def __call__(self, args):
        if args.version:
            print(__version__)
            return

        return super().__call__(args)

