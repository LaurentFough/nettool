# -*- coding: utf-8 -*-

from nettool.address.transport_address import TransportAddress
from nettool.address.transport_address_builder import TransportAddressBuilder
from nettool.address.tcp_address import TcpAddress
from nettool.address.udp_address import UdpAddress
from nettool.address.address_group import AddressGroup


class TransportGroup(AddressGroup):
    _address_name = 'Transport'
    _default_address = TransportAddress()
    _address_type = (TransportAddress, TcpAddress, UdpAddress)

    def __init__(self, name=None):
        self.name = name
        self._addresses = list()

    @staticmethod
    def address_builder(address):
        return TransportAddressBuilder.build(address)

    @staticmethod
    def from_string(value):
        transport_address = TransportAddress.from_string(value)
        transport_group = TransportGroup()
        transport_group.add(transport_address)
        return transport_group

    @staticmethod
    def _is_member(key, member):
        return key in member
