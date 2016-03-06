# -*- coding: utf-8 -*-

import ipaddress


class IPv4Address(ipaddress.IPv4Address):

    def __init__(self, address):
        if not isinstance(address, basestring):
            raise TypeError("Invalid type used in IP initilization: '{}'. Must use a string".format(type(address).__name__))
        if isinstance(address, str):
            address = unicode(address)
        try:
            super(IPv4Address, self).__init__(address)
        except ipaddress.AddressValueError as e:
            raise ValueError(e)

    def __eq__(self, value):
        if isinstance(value, basestring):
            return value == self.exploded
        return super(IPv4Address, self).__eq__(value)
