# -*- coding: utf-8 -*-

from nettool.address.transport_group import TransportGroup
from nettool.utilities import raise_type_exception


class TransportLayer(object):

    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination

    @staticmethod
    def _build_transport_group(value):
        if value is None:
            value = TransportGroup()
        elif isinstance(value, basestring):
            value = TransportGroup.from_string(value)
        if not isinstance(value, TransportGroup):
            message = 'Invalid type  {}'
            message = message.format(type(value).__name__)
            raise TypeError(message)
        return value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = TransportLayer._build_transport_group(value)

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = TransportLayer._build_transport_group(value)

    def __repr__(self):
        output = ''
        for side_attr in ('source', 'destination'):
            name = "{}".format(str(getattr(self, side_attr)))
            output = ' '.join([output, name])
        class_name = self.__class__.__name__
        return '<{}{}>'.format(class_name, output).replace('  ', ' ')

    def __eq__(self, key):
        if not isinstance(key, TransportLayer):
            raise_type_exception(key, (TransportLayer, ), 'test equality of')
        return self.source == key.source and self.destination == key.destination

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if isinstance(key, TransportLayer):
            for side in ('source', 'destination'):
                for key_address in getattr(key, side).addresses:
                    if key_address not in getattr(self, side):
                        return False
            return True
        raise_type_exception(key, (TransportLayer, ), 'test membership of')
