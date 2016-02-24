# -*- coding: utf-8 -*-

from nettool.transport_address import TransportAddress
from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress
from nettool._tools import raise_type_exception
from nettool.address_group import AddressGroup


class TransportGroup(AddressGroup):
    _default_name = 'Transport Group'
    _default_address = TransportAddress()
    _address_type = (TransportAddress, TcpAddress, UdpAddress)

    def __init__(self, name=None):
        self.name = name
        self._addresses = list()

    @staticmethod
    def address_from_string(address):
        if isinstance(address, (basestring, int)):
            address = TransportAddress.from_string(address)
        elif not isinstance(address, TransportAddress):
            raise_type_exception(address, (TransportAddress, ), 'add')
        return address

    @staticmethod
    def from_string(value):
        transport_address = TransportAddress.from_string(value)
        transport_group = TransportGroup()
        transport_group.add(transport_address)
        return transport_group

    @staticmethod
    def _is_member(key, member):
        return key in member
