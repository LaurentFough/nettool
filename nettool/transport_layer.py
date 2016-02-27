# -*- coding: utf-8 -*-

from nettool.transport_group import TransportGroup
# from nettool.transport_address import TransportAddress
from nettool._tools import raise_type_exception
from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress


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

    @staticmethod
    def _clean_build_string(value):
        replacements = (('-', ' '), ('  ', ' '))
        for match, replacement in replacements:
            value = value.replace(match, replacement)
        return value.lower().strip()

    @classmethod
    def from_string(cls, value):
        if isinstance(value, basestring):
            values = cls._clean_build_string(value).split()
            # tcp 1 2 --> tcp 1 1 2 2
            if len(values) is 3:
                values = '{v[0]} {v[1]} {v[1]} {v[2]} {v[2]}'.format(v=values)
                values = values.split()
            if len(values) is 5:
                protocol_cls = None
                for protocol in (TcpAddress, UdpAddress):
                    if protocol._address_name.lower() == values[0]:
                        protocol_cls = protocol
                        break
                if protocol_cls is not None:
                    sides = list()
                    for low, high in ((values[1], values[2]), (values[3], values[4])):
                        side = TransportGroup()
                        port_string = '{}-{}'.format(low, high)
                        port_address = protocol_cls.from_string(port_string)
                        side.add(port_address)
                        sides.append(side)
                        return cls(*sides)
            message = 'Unsupported string initialization format \'{}\''
            message = message.format(value)
            raise ValueError(message)
        raise_type_exception(value, (str, unicode), 'build from')

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
            name = "'{}'".format(getattr(self, side_attr).name)
            output = ' '.join([output, name])
        class_name = self.__class__.__name__
        return '<{}{}>'.format(class_name, output)

    def __eq__(self, key):
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
