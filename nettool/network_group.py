# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface, IPv4Network
# from nettool.transport_address import TransportAddress
from nettool._tools import raise_type_exception
from nettool.address_group import AddressGroup
from nettool.nutility import NUtility as nu


class NetworkGroup(AddressGroup):
    _default_name = 'Network Group'
    _default_address = IPv4Network(u'0.0.0.0/0')

    @staticmethod
    def _clean_address(network):
        if network is None:
            network = NetworkGroup._default_address
        else:
            nu.validate.network(network, raise_exception=True)
            network = IPv4Interface(unicode(network)).network
        return network

    @staticmethod
    def _build_address(value):
        if isinstance(value, (basestring)):
            value = IPv4Interface(unicode(value)).network
        elif not isinstance(value, IPv4Network):
            raise_type_exception(value, (IPv4Network, ), 'build with')
        return value

    @staticmethod
    def from_string(value):
        address = NetworkGroup._build_address(value)
        group = NetworkGroup()
        group.add(address)
        return group

    def __contains__(self, key):
        if isinstance(key, (basestring)):
            value = NetworkGroup._build_address(key)
        valid_types = (IPv4Network, NetworkGroup)
        if not isinstance(value, valid_types):
            raise_type_exception(key, valid_types, 'test membership of')
        if isinstance(key, NetworkGroup):
            found = False
            for key_address in key.addresses:
                for self_address in self.addresses:
                    if key_address in self_address:
                        found = True
                        break
                if not found:
                    return False
                found = False
            return True
        elif isinstance(key, IPv4Network):
            for address in self.addresses:
                if key.subnet_of(address):
                    return True
            return False
        return False
