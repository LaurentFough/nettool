# -*- coding: utf-8 -*-
from nettool._tools import raise_type_exception


class LoggingFacility(object):
    _level_names = [
        'emergency',
        'alert',
        'critical',
        'error',
        'warning',
        'notification',
        'information',
        'debug',
    ]

    def __init__(self, level=None):
        self.level = level

    @property
    def number(self):
        return self.level

    @property
    def name(self):
        name = 'none'
        if self.level is not None:
            name = self._level_names[self.level]
        return name

    @property
    def level(self):
        return self._level

    @classmethod
    def from_string(cls, value):
        if not isinstance(value, (basestring, int)):
            raise_type_exception(value, (cls, ), 'build from')
        return cls(value)

    @level.setter
    def level(self, value):
        original_value = value
        if value is None:
            self._level = None
            return
        elif isinstance(value, basestring):
            value = value.strip().lower()
            if value.isdigit():
                value = int(value)
            else:
                if value in self._level_names:
                    value = self._level_names.index(value)
                else:
                    message = 'No logging level name \'{}\''.format(original_value)
                    raise ValueError(message)
        elif isinstance(value, int) and not isinstance(value, bool):
            if value not in range(len(self._level_names)):
                message = 'Invalid logging level {}'.format(original_value)
                raise ValueError(message)

        if not isinstance(value, int) or isinstance(value, bool):
            raise_type_exception(value, (int, str), 'set')
        self._level = value

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __eq__(self, key):
        if not isinstance(key, LoggingFacility):
            key = self.from_string(key)
        return key.level == self.level

    def __contains__(self, key):
        value = key
        if not isinstance(key, (basestring, int, LoggingFacility)):
            raise_type_exception(key, (LoggingFacility), 'test memebership of')
        if not isinstance(key, LoggingFacility):
            value = self.from_string(value)
        return value.level <= self.level
