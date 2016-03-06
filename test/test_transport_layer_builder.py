# -*- coding: utf-8 -*-

from nose.tools import assert_is_instance, assert_raises, assert_equals

from nettool.transport_layer import TransportLayer
from nettool.transport_layer_builder import TransportLayerBuilder
from nettool.transport_group import TransportGroup
from nettool.transport_address import TransportAddress
from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress


class TestTransportLayerBuilder(object):

    def setup(self):
        self.build = TransportLayerBuilder.build

    def test_build_invalid_type(self):
        invalid_types = (
            True,
        )
        for value in invalid_types:
            assert_raises(TypeError, self.build, value)

    def test_build_invalid_strings(self):
        invalid_strings = (
            'True',
            'tcp 0-0 0-0',
            'udp 0-0 0-0',
            '0-0 0-0',
        )
        for value in invalid_strings:
            assert_raises(ValueError, self.build, value)

    def test_build_integer(self):
        transport = self.build(22)
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], TransportAddress)
        assert_is_instance(transport.destination[0], TransportAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 22)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_single_port(self):
        transport = self.build('22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], TransportAddress)
        assert_is_instance(transport.destination[0], TransportAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 22)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_tcp_single_port(self):
        transport = self.build('tcp 22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], TcpAddress)
        assert_is_instance(transport.destination[0], TcpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 22)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_udp_single_port(self):
        transport = self.build('udp 22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], UdpAddress)
        assert_is_instance(transport.destination[0], UdpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 22)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_destination_port_range(self):
        transport = self.build('1 22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], TransportAddress)
        assert_is_instance(transport.destination[0], TransportAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 1)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_destination_tcp_port_range(self):
        transport = self.build('tcp 1 22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.source[0], TcpAddress)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.destination[0], TcpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 1)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_destination_udp_port_range(self):
        transport = self.build('udp 1 22')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.source[0], UdpAddress)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.destination[0], UdpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 65535)
        assert_equals(transport.destination[0].low, 1)
        assert_equals(transport.destination[0].high, 22)

    def test_build_string_full(self):
        transport = self.build('1 2 3 4')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.source[0], TransportAddress)
        assert_is_instance(transport.destination[0], TransportAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 2)
        assert_equals(transport.destination[0].low, 3)
        assert_equals(transport.destination[0].high, 4)

    def test_build_string_tcp_full(self):
        transport = self.build('tcp 1 2 3 4')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.source[0], TcpAddress)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.destination[0], TcpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 2)
        assert_equals(transport.destination[0].low, 3)
        assert_equals(transport.destination[0].high, 4)

    def test_build_string_udp_full(self):
        transport = self.build('udp 1 2 3 4')
        assert_is_instance(transport, TransportLayer)
        assert_is_instance(transport.source, TransportGroup)
        assert_is_instance(transport.source[0], UdpAddress)
        assert_is_instance(transport.destination, TransportGroup)
        assert_is_instance(transport.destination[0], UdpAddress)
        assert_equals(transport.source[0].low, 1)
        assert_equals(transport.source[0].high, 2)
        assert_equals(transport.destination[0].low, 3)
        assert_equals(transport.destination[0].high, 4)
