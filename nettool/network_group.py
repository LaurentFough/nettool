# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface, IPv4Network, AddressValueError
from nettool._tools import raise_type_exception
from nettool.address_group import AddressGroup
from nettool.nutility import NUtility as nu


class NetworkGroup(AddressGroup):
    _default_name = 'Network Group'
    _default_address = IPv4Network(u'0.0.0.0/0')
    _address_type = (IPv4Network, )

    @staticmethod
    def _clean_address(network):
        if network is None:
            network = NetworkGroup._default_address
        else:
            nu.validate.network(network, raise_exception=True)
            network = IPv4Interface(unicode(network)).network
        return network

    @staticmethod
    def address_from_string(value):
        if isinstance(value, (basestring)):
            try:
                value = IPv4Interface(unicode(value)).network
            except AddressValueError:
                message = 'Unsupported string initialization format \'{}\''
                message = message.format(value)
                raise ValueError(message)
        elif not isinstance(value, IPv4Network):
            raise_type_exception(value, (IPv4Network, ), 'build with')
        return value

    @staticmethod
    def _is_member(key, member):
        return key.subnet_of(member)

    @staticmethod
    def from_string(value):
        address = NetworkGroup.address_from_string(value)
        group = NetworkGroup()
        group.add(address)
        return group
