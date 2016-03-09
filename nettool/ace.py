# -*- coding: utf-8 -*-

from nettool.layer.network_layer import NetworkLayer
from nettool.layer.transport_layer_builder import TransportLayerBuilder
from nettool.logging_facility import LoggingFacility
from nettool.utilities import raise_type_exception


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
        if value is not None:
            value = TransportLayerBuilder.build(value)
        self._transport = value

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
                if isinstance(key.transport, type(self.transport)) and \
                        key.transport == self.transport:
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
                if self._transport is None or \
                    (isinstance(key.transport, type(self.transport)) and
                        key.transport in self.transport):
                    return key.network in self.network
        return False

    def __repr__(self):
        cls_name = self.__class__.__name__.upper()
        return '<{} {}>'.format(cls_name, self.__str__())

    def _iter_networks(self, groups=False):
        source_networks = self.network.source.addresses
        destination_networks = self.network.destination.addresses
        if groups and self.network.source.name is not None:
            source_networks = [self.network.source.name]
        if groups and self.network.destination.name is not None:
            destination_networks = [self.network.destination.name]

        for src_net in source_networks:
            for dst_net in destination_networks:
                yield src_net, dst_net

    def _iter_transport(self, groups=False):
        source_ports = [None]
        destination_ports = [None]
        if self.transport is not None:
            source_ports = self.transport.source.addresses
            destination_ports = self.transport.destination.addresses
            if groups and self.transport.source.name is not None:
                source_ports = [self.transport.source.name]
            if groups and self.transport.destination.name is not None:
                destination_ports = [self.transport.destination.name]
        for src_port in source_ports:
            for dst_port in destination_ports:
                yield src_port, dst_port

    def _iter_layers(self, groups=False):
        for src_net, dst_net in self._iter_networks(groups=groups):
            for src_port, dst_port in self._iter_transport(groups=groups):
                yield src_net, src_port, dst_net, dst_port

    def __str__(self):
        return self._print(groups=False)

    def print_group(self):
        return self._print(groups=True)

    def _print(self, groups=True):
        permission = 'permit'
        if not self.permit:
            permission = 'deny'
        output = list()
        for src_net, src_port, dst_net, dst_port in self._iter_layers(groups=groups):
            line = list()
            line.append(permission)
            if self.transport is not None:
                line.append(self.transport.destination[0].type.lower())
            else:
                line.append('ip')
            line.append(str(src_net))
            if src_port is not None and src_port != src_port.__class__():
                if isinstance(src_port, basestring):
                    line.append(src_port)
                else:
                    line.append(src_port._port_string())
            line.append(str(dst_net))
            if dst_port is not None and dst_port != dst_port.__class__():
                if isinstance(dst_port, basestring):
                    line.append(dst_port)
                else:
                    line.append(dst_port._port_string())
            if self.logging.level is not None:
                line.append(self.logging.name)
            output.append(' '.join(line).replace('  ', ' ').strip())
        return '\r\n'.join(output).replace('  ', ' ').strip()
