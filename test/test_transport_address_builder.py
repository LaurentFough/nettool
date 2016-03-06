# -*- coding: utf-8 -*-

from nose.tools import assert_is_instance, assert_raises, assert_equals

from nettool.address.transport_address_builder import TransportAddressBuilder
from nettool.address.transport_address import TransportAddress
from nettool.address.tcp_address import TcpAddress
from nettool.address.udp_address import UdpAddress


class TestTransportAddressBuilder(object):

    def setup(self):
        self.build = TransportAddressBuilder.build

    def test_build_invalid_type(self):
        invalid_types = (
            True,
        )
        for value in invalid_types:
            assert_raises(TypeError, self.build, value)

    def test_build_invalid_strings(self):
        invalid_strings = (
            'True',
        )
        for value in invalid_strings:
            assert_raises(ValueError, self.build, value)

    def test_tcp_build(self):
        build_protocols = (
            ('', TransportAddress),
            ('tcp', TcpAddress),
            ('udp', UdpAddress),
        )
        build_ports = (
            (22, 22),
            (1, 2),
        )
        seperators = (
            ' ',
            '-',
        )
        for protcol_text, protocol_cls in build_protocols:
            for low, high in build_ports:
                for seperator in seperators:
                    port_string = '{}{}{}'.format(low, seperator, high)
                    if low == high:
                        port_string = '{}'.format(low)
                    instance = self.build('{} {}'.format(protcol_text, port_string).strip())
                    assert_is_instance(instance, protocol_cls)
                    assert_equals(instance.low, low)
                    assert_equals(instance.high, high)
