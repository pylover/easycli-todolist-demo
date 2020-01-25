import functools

from easycli import Root, SubCommand, Argument

from . import db


def listcompleter(prefix, action, parser, parsed_args):
    return set(l for l, _ in db.getall())


def itemcompleter(prefix, action, parser, parsed_args):
    list_ = parsed_args.list
    return list(i for l, i in db.getall() if l == list_)


ListArgument = functools.partial(
    Argument,
    'list',
    default='',
    help='List name',
    completer=listcompleter
)


ItemArgument = functools.partial(
    Argument,
    'item',
    help='Item name',
    completer=itemcompleter
)


class Delete(SubCommand):
    __command__ = 'delete'
    __aliases__ = ['d']
    __arguments__ = [
        ListArgument(),
        ItemArgument(),
    ]

    def __call__(self, args):
        db.delete(args.list, args.item)


class Show(SubCommand):
    __command__ = 'show'
    __aliases__ = ['s', 'l']
    __arguments__ = [
        ListArgument(nargs='?')
    ]

    def __call__(self, args):
        if args.list:
            for l, i in db.getall():
                if l == args.list:
                    print(i)

        else:
            for l, i in db.getall():
                print(f'{l}\t{i}')


class Append(SubCommand):
    __command__ = 'append'
    __aliases__ = ['add', 'a']
    __arguments__ = [
        ListArgument(),
        ItemArgument(),
    ]

    def __call__(self, args):
        db.append(args.list, args.item)


class Todo(Root):
    __help__ = 'Simple todo list'
    __completion__ = True
    __arguments__ = [
        Append,
        Show,
        Delete,
    ]

