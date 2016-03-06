# -*- coding: utf-8 -*-

from nettool.address.transport_address import TransportAddress


class UdpAddress(TransportAddress):
    _address_name = 'UDP'
    type = 'UDP'
