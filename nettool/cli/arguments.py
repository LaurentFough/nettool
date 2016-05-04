# -*- coding: utf-8 -*-

import click

from nettool.click.validation import ArgumentValidation


class Argument(object):
    hostname = click.Argument(
        ['hostname'],
        type=unicode,
        nargs=1,
        callback=ArgumentValidation.hostname
    )
    ip = click.Argument(
        ['ip'],
        type=unicode,
        nargs=1,
        callback=ArgumentValidation.ip
    )
    relm = click.Argument(
        ['relm'],
        type=unicode,
        nargs=1,
        callback=ArgumentValidation.relm
    )
    device_type = click.Argument(
        ['device_type'],
        type=unicode,
        nargs=1,
        callback=ArgumentValidation.device_type
    )
    search_term = click.Argument(
        ['search_term'],
        type=unicode,
        nargs=-1,
        callback=ArgumentValidation.search_term
    )
