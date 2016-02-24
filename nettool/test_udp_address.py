# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_in, assert_not_in

from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress


class TestUdpAddress(object):

    def setup(self):
        self.address = UdpAddress()
        self.address.low = 1
        self.address.high = 2

    def test_repr(self):
        assert_equals(self.address.__repr__(), "<UdpAddress 1-2>")

    def test_str(self):
        assert_equals(self.address.__str__(), "UDP 1-2")

    def test_contains(self):
        udp_port = UdpAddress.from_string('1')
        udp_ports = UdpAddress.from_string('1-3')
        assert_in(udp_port, udp_ports)

    def test_not_contains(self):
        udp_port = UdpAddress.from_string('1')
        tcp_ports = TcpAddress.from_string('1-3')
        assert_not_in(udp_port, tcp_ports)
