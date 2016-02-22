# -*- coding: utf-8 -*-

from ipaddress import IPv4Network
from nose.tools import assert_equals, assert_true, assert_raises
from nose.tools import assert_false, assert_in, assert_not_in, assert_is_instance
from nettool.network_group import NetworkGroup


class TestNetworkGroup(object):

    def setup(self):
        self.invalid_types = (True, False, 1)
        self.address01 = IPv4Network(u'10.0.0.0/8')
        self.address02 = IPv4Network(u'192.168.0.0/16')
        self.address03 = IPv4Network(u'172.16.0.0/12')

    def test_addresses_getter(self):
        group = NetworkGroup()
        assert_equals(group.addresses, [NetworkGroup._default_address])

    def test_add(self):
        group = NetworkGroup()
        address04 = IPv4Network(u'10.0.0.0/8')
        assert_true(group.add(self.address01))
        assert_false(group.add(self.address01))
        assert_true(group.add(self.address02))
        assert_false(group.add(self.address02))
        assert_false(group.add(self.address01))
        assert_false(group.add(address04))

    def test_build_address_invalid(self):
        for value in self.invalid_types:
            assert_raises(TypeError, NetworkGroup._build_address, value)

    def test_has(self):
        group = NetworkGroup()
        addresses = list()
        addresses.append(self.address01)
        addresses.append(self.address02)
        addresses.append(self.address03)
        for index, address in enumerate(addresses):
            for added in addresses[:index]:
                assert_true(group.has(added))
            for not_added in addresses[index:]:
                assert_false(group.has(not_added))
            group.add(address)

    def test_remove(self):
        group = NetworkGroup()
        group.add(self.address01)
        assert_false(group.remove(self.address02))
        group.add(self.address02)
        assert_true(group.remove(self.address01))
        assert_true(group.remove(self.address02))
        assert_false(group.remove(self.address01))
        assert_false(group.has(self.address01))
        assert_false(group.has(self.address02))

    def test_repr(self):
        pass
        # TODO: Finish testing NetworkGroup and Fix TransportGroup to inherit AddressGroup

    def test_equality(self):
        pass

    def test_inequality(self):
        pass

    def test_contains_single_port(self):
        pass

    def test_contains_transport_layer(self):
        pass

    def test_from_string(self):
        pass
