# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_not_equals, assert_true
from nose.tools import assert_false, assert_in, assert_not_in, assert_is_instance

from nettool.transport_group import TransportGroup
from nettool.transport_address import TransportAddress
from nettool.tcp_address import TcpAddress
from nettool.udp_address import UdpAddress


class TestTransportGroup(object):

    def setup(self):
        # self.invalid_name_values = (0, 65536)
        self.invalid_name_types = (True, False, 1)
        self.group = TransportGroup()

    def test_initialization_defaults(self):
        group = TransportGroup()
        assert_equals(group.name, TransportGroup._default_name)

    def test_initialization(self):
        assert_equals(TransportGroup('name').name, 'name')

    def test_initialization_invalid(self):
        for value in self.invalid_name_types:
            assert_raises(TypeError, TransportGroup, value)

    def test_name_setter(self):
        group = TransportGroup()
        for value in ('test01', 'test02', ):
            group.name = value
            assert_equals(group.name, value)

    def test_addresses_getter(self):
        group = TransportGroup()
        assert_equals(group.addresses, [TransportAddress()])

    def test_name_setter_invalid(self):
        group = TransportGroup()
        for value in self.invalid_name_types:
            assert_raises(TypeError, setattr, group, 'name', value)

    def test_add(self):
        group = TransportGroup()
        address01 = TransportAddress(1, 3)
        address02 = TransportAddress(3, 5)
        address03 = TransportAddress(25, 27)
        assert_true(group.add(address01))
        assert_false(group.add(address01))
        assert_false(group.add('1 3'))
        assert_true(group.add(address02))
        assert_false(group.add(address02))
        assert_false(group.add('3 - 5'))
        assert_false(group.add(address01))
        assert_true(group.add('25-27'))
        assert_false(group.add(address03))

    def test_add_mixed_ports(self):
        group = TransportGroup()
        group.add(TransportAddress.from_string('1-3'))
        group.add(TcpAddress.from_string('1-3'))
        group.add(UdpAddress.from_string('1-3'))
        assert_equals(len(group), 3)

    def test_address_from_string_invalid(self):
        group = TransportGroup()
        assert_raises(TypeError, group.address_from_string, True)

    def test_has(self):
        group = TransportGroup()
        addresses = list()
        addresses.append(TransportAddress(1, 3))
        addresses.append(TransportAddress(3, 5))
        addresses.append(TransportAddress(25, 27))
        for index, address in enumerate(addresses):
            for added in addresses[:index]:
                assert_true(group.has(added))
            for not_added in addresses[index:]:
                assert_false(group.has(not_added))
            group.add(address)

    def test_remove(self):
        group = TransportGroup()
        address01 = TransportAddress(1, 3)
        address02 = TransportAddress(3, 5)
        group.add(address01)
        assert_false(group.remove(address02))
        group.add(address02)
        assert_true(group.remove(address01))
        assert_true(group.remove(address02))
        assert_false(group.remove(address01))
        assert_false(group.has(address01))
        assert_false(group.has(address02))

    def test_repr(self):
        layer = TransportGroup()
        layer.add('1-2')
        assert_equals(layer.__repr__(), "<TransportGroup ['Port 1-2']>")
        layer.add('3-4')
        assert_equals(layer.__repr__(), "<TransportGroup ['Port 1-2', 'Port 3-4']>")
        layer.add('5-6')
        text = "<TransportGroup ['Port 1-2', 'Port 3-4', 'Port 5-6']>"
        assert_equals(layer.__repr__(), text)
        layer.add('7-8')
        text = "<TransportGroup ['Port 1-2', 'Port 3-4', 'Port 5-6', ...]>"
        assert_equals(layer.__repr__(), text)

    def test_equality(self):
        group_a = TransportGroup()
        group_b = TransportGroup()
        addresses = list()
        addresses.append(TransportAddress(1, 3))
        addresses.append(TransportAddress(3, 5))
        addresses.append(TransportAddress(25, 27))
        assert_equals(group_a, group_b)
        for address in addresses:
            group_a.add(address)
            group_b.add(address)
            assert_equals(group_a, group_b)

    def test_inequality(self):
        group_a = TransportGroup()
        group_b = TransportGroup()
        address01 = TransportAddress(1, 3)
        address02 = TransportAddress(3, 5)
        assert_equals(group_a, group_b)
        group_a.add(address01)
        assert_not_equals(group_a, group_b)
        group_b.add(address01)
        assert_equals(group_a, group_b)
        group_b.add(address02)
        assert_not_equals(group_a, group_b)

    def test_contains_single_port(self):
        group = TransportGroup()
        assert_in(2, group)
        group.add('1-2')
        assert_in(1, group)
        assert_not_in(3, group)

    def test_contains_transport_layer(self):
        group = TransportGroup()
        address = TransportAddress(low=1, high=2)
        assert_in(address, group)
        group.add('1-2')
        assert_in(address, group)
        assert_not_in('3-4', group)

    def test_from_string(self):
        from_string = TransportGroup.from_string
        group = from_string(1)
        assert_is_instance(group, TransportGroup)
        address = TransportAddress.from_string(1)
        assert_in(address, group)
