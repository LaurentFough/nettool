# -*- coding: utf-8 -*-


def list_repr(the_list, max_entires=3):
    """ Sortens the string representation of a long list"""
    max_entires -= 1
    entries = list()
    for index, item in enumerate(the_list):
        if index > max_entires:
            entries.append('...')
            break
        entries.append(item.__str__())
    return str(entries).replace("'...'", '...')
