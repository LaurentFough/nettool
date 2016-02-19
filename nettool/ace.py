# -*- coding: utf-8 -*-

from ip_layer import IPLayer
from protocol_layer import ProtocolLayer


class Ace(object):

    def __init__(self, acl_type=None, line_number=None, permit=None,
                 protocol=None, source=None, source_port_low=None,
                 source_port_high=None, source_established=None, destination=None,
                 destination_port_low=None, destination_port_high=None, destination_established=None,
                 logging=None, hits=None):
        self._protocol_layer = ProtocolLayer(protocol)
        self._ip_layer = IPLayer(source, destination)

        self.acl_type = acl_type
        self.line_number = line_number
        self.permit = permit
        if permit is None:
            self.permit = True
        self.source = source
        self.destination = destination
        for network in (source, destination):
            if network:
                network = unicode(network)

        # self.source_port_low = source_port_low or cls.min_port
        # self.source_port_high = source_port_high or cls.max_port
        # self.source_established = source_established or cls.default_established
        # self.destination_port_low = destination_port_low or cls.min_port
        # self.destination_port_high = destination_port_high or cls.max_port
        # self.destination_established = destination_established or cls.default_established
        self.logging = logging
        self.hits = hits

    @property
    def protocol(self):
        return self._protocol_layer.name

    @protocol.setter
    def protocol(self, value):
        self._protocol_layer.name = value

    @property
    def source(self):
        return self._ip_layer.source

    @source.setter
    def source(self, value):
        self._ip_layer.source = value

    @property
    def destination(self):
        return self._ip_layer.destination

    @destination.setter
    def destination(self, value):
        self._ip_layer.destination = value
