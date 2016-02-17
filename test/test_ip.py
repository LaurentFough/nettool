# -*- coding: utf-8 -*-

from nettool.ipv4address import IPv4Address

from nose.tools import assert_equals


class TestIPAddress(object):

    def test_initilization(self):
        ip = IPv4Address('1.2.3.4')
        assert_equals(ip.exploded, '1.2.3.4')
