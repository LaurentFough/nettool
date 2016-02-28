# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_in, assert_not_in

from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress


class TestTcpAddress(object):

    def setup(self):
        self.address = TcpAddress()
        self.address.low = 1
        self.address.high = 2

    def test_initialization(self):
        assert_equals(self.address.type, 'TCP')

    def test_repr(self):
        assert_equals(self.address.__repr__(), "<TcpAddress 1-2>")

    def test_str(self):
        assert_equals(self.address.__str__(), "TCP 1-2")

    def test_contains(self):
        tcp_port = TcpAddress.from_string('1')
        tcp_ports = TcpAddress.from_string('1-3')
        assert_in(tcp_port, tcp_ports)

    def test_not_contains(self):
        tcp_port = TcpAddress.from_string('1')
        udp_ports = UdpAddress.from_string('1-3')
        assert_not_in(tcp_port, udp_ports)
