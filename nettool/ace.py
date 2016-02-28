# -*- coding: utf-8 -*-

from nettool.network_layer import NetworkLayer
from nettool.transport_layer import TransportLayer
from nettool.logging_facility import LoggingFacility
from nettool._tools import raise_type_exception


class Ace(object):

    def __init__(self, permit=None,
                 network=None, transport=None,
                 logging=None, hits=None):
        self.permit = True
        if permit is not None or permit is False:
            self.permit = False
        self.hits = hits or 0

        self.network = network
        self.transport = transport
        self.logging = logging

    @property
    def logging(self):
        return self._logging

    @logging.setter
    def logging(self, value):
        self._logging = self._type_initialization(value, LoggingFacility)

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = self._type_initialization(value, NetworkLayer)

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, value):
        self._transport = self._type_initialization(value, TransportLayer)

    @staticmethod
    def _type_initialization(value, cls):
        if value is None:
            value = cls()
        elif not isinstance(value, cls):
            value = cls.from_string(value)
        if not isinstance(value, cls):
            raise_type_exception(value, (cls, ), 'build from')
        return value

    def __eq__(self, key):
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__, ), 'test equality of')
        if key.permit == self.permit:
            if key.logging == self.logging:
                if key.transport == self.transport:
                    return key.network == self.network
        return False

    def __ne__(self, key):
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__, ), 'test equality of')
        return not self.__eq__(key)

    def __contains__(self, key):
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__, ), 'test membership of')
        if key.permit == self.permit:
            if key.logging in self.logging:
                if key.transport in self.transport:
                    return key.network in self.network
        return False

    def __repr__(self):
        cls_name = self.__class__.__name__.upper()
        return '<{} {}>'.format(cls_name, self.__str__())

    def __str__(self):
        output = list()
        permit = 'permit'
        if not self.permit:
            permit = 'deny'
        output.append(permit)
        output.append(self.network.source.name)
        output.append(self.transport.source.name)
        output.append(self.network.destination.name)
        output.append(self.transport.destination.name)
        if self.logging.level is not None:
            output.append(self.logging.name)
        return ' '.join(output)
