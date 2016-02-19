# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface
from nettool.nutility import NUtility as nu


class IPLayer(object):
    _default_network = IPv4Interface(u'0.0.0.0/0')

    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination

    @staticmethod
    def _clean_network(network):
        if network is None:
            network = IPLayer._default_network
        else:
            nu.validate.network(network, raise_exception=True)
            network = IPv4Interface(unicode(network)).network
        return network

    @property
    def source(self):
        return self._source.exploded

    @source.setter
    def source(self, value):
        self._source = IPLayer._clean_network(value)

    @property
    def destination(self):
        return self._destination.exploded

    @destination.setter
    def destination(self, value):
        self._destination = IPLayer._clean_network(value)
