# -*- coding: utf-8 -*-

from nettool.address.transport_address import TransportAddress


class TcpAddress(TransportAddress):
    _address_name = 'TCP'
    type = 'TCP'
