# -*- coding: utf-8 -*-

import click

from nettool.nettest import NetTest as ntest


class ArgumentValidation(object):
    @classmethod
    def _type_validation(cls, validation_type, value):
        try:
            getattr(ntest.validate, validation_type)(value, raise_exception=True)
        except ValueError as e:
            error = unicode(e)
            raise click.BadParameter(error)
        return value

    @classmethod
    def _format_error(cls, error, valid_options):
        if valid_options:
            valid = u'\n\t\t'.join(valid_options)
            message = u'{}\n\tThe valid options are:\n\t\t{}'.format(error, valid)
        else:
            message = u'{}. There are no valid options.'.format(error)
        return message

    @classmethod
    def _type_validation_with_suggestions(cls, validation_class, value):
        try:
            validation_class.valid(value, raise_exception=True)
        except ValueError as e:
            error = unicode(e)
            message = cls._format_error(error, validation_class.valid_entries)
            raise click.BadParameter(message)
        return value

    @classmethod
    def search_term(cls, ctx, param, value):
        if isinstance(value, tuple):
            value = ' '.join(value)
            if not value:
                return '*'
        if not isinstance(value, basestring):
            raise click.BadParameter('Invalid search term')
        value = '*{}*'.format(value).replace('**', '*')
        return value

    @classmethod
    def hostname(cls, ctx, param, value):
        return cls._type_validation('hostname', value)

    @classmethod
    def ip(cls, ctx, param, value):
        return cls._type_validation('ip', value)
