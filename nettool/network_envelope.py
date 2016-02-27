# -*- coding: utf-8 -*-

from nettool._tools import raise_type_exception


class NetworkEnvelope(object):
    _group_type = None

    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination

    @classmethod
    def from_string(cls, value):
        if isinstance(value, basestring):
            value = cls._clean_build_string(value)
            values = value.split()
            if len(values) == 2:
                envelope = cls()
                for index, side in enumerate(('source', 'destination')):
                    address_group = cls._group_from_string(values[index])
                    setattr(envelope, side, address_group)
                return envelope
            message = 'Unsupported string initialization format \'{}\''
            message = message.format(value)
            raise ValueError(message)
        raise_type_exception(value, (str, unicode), 'build from')

    @classmethod
    def _group_from_string(cls, value):
        address_group = cls._group_type.from_string(value)
        return address_group

    @staticmethod
    def _clean_build_string(value):
        return value.strip().replace('  ', ' ')

    @classmethod
    def _clean_side(cls, value):
        if value is not None:
            if isinstance(value, basestring):
                value = cls._group_from_string(value)
            if not isinstance(value, cls._group_type):
                raise_type_exception(value, (cls._group_type,), 'set')
        return value

    @property
    def source(self):
        value = self._source
        if value is None:
            value = self._group_type()
        return value

    @source.setter
    def source(self, value):
        value = self._clean_side(value)
        self._source = value

    @property
    def destination(self):
        value = self._destination
        if value is None:
            value = self._group_type()
        return value

    @destination.setter
    def destination(self, value):
        value = self._clean_side(value)
        self._destination = value

    def __repr__(self):
        class_name = self.__class__.__name__
        return '<{} {} {}>'.format(class_name, self.source, self.destination)

    def __eq__(self, key):
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__,), 'test equality of')
        return self.source == key.source and \
            self.destination == key.destination

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__,), 'test membership of')
        for side in ('source', 'destination'):
            if getattr(key, side) not in getattr(self, side):
                return False
        return True
