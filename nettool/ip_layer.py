# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface
from nettool.nutility import NUtility as nu


class IPLayer(object):
    _default_network = IPv4Interface(u'0.0.0.0/0')

    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination

    @staticmethod
    def from_string(value):
        if isinstance(value, basestring):
            value = IPLayer._clean_ip_layer_string(value)
            networks = value.split()
            if len(networks) == 2:
                source, destination = networks
                valid = nu.validate.network(source)
                valid = valid and nu.validate.network(destination)
                if valid:
                    return IPLayer(source=source, destination=destination)
        message = 'Unsupported string initializer \'{}\''
        message = message.format(value)
        raise ValueError(message)

    @staticmethod
    def _clean_ip_layer_string(value):
        return value.strip().replace('  ', ' ')

    @staticmethod
    def _clean_network(network):
        if network is None:
            network = IPLayer._default_network
        else:
            nu.validate.network(network, raise_exception=True)
            network = IPv4Interface(unicode(network))
        return network

    @property
    def source(self):
        return self._source.network.exploded

    @source.setter
    def source(self, value):
        self._source = IPLayer._clean_network(value)

    @property
    def destination(self):
        return self._destination.network.exploded

    @destination.setter
    def destination(self, value):
        self._destination = IPLayer._clean_network(value)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '<{} {} {}>'.format(class_name, self.source, self.destination)

    def __eq__(self, key):
        if not isinstance(key, IPLayer):
            class_name = self.__class__.__name__
            message = 'Cannot test equality of class {} to {}.'
            message = message.format(type(key).__name__, class_name)
            raise TypeError(message)
        return self.source == key.source and \
            self.destination == key.destination

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if not isinstance(key, IPLayer):
            class_name = self.__class__.__name__
            message = 'Cannot test if {} contains {} types.'
            message = message.format(class_name, type(key).__name__)
            raise TypeError(message)
        return key._source.network.subnet_of(self._source.network) and \
            key._destination.network.subnet_of(self._destination.network)
