# -*- coding: utf-8 -*-

from ipaddress import IPv4Network
from nose.tools import assert_equals, assert_not_equals, assert_true, assert_raises
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

    def test_addresses_getitem(self):
        group = NetworkGroup()
        assert_equals(group.addresses[0], IPv4Network(u'0.0.0.0/0'))

    def test_add(self):
        group = NetworkGroup()
        address04 = IPv4Network(u'10.0.0.0/8')
        assert_true(group.add(self.address01))
        assert_false(group.add(self.address01))
        assert_true(group.add(self.address02))
        assert_false(group.add(self.address02))
        assert_false(group.add(self.address01))
        assert_false(group.add(address04))

    def test_address_from_string_invalid(self):
        for value in self.invalid_types:
            assert_raises(TypeError, NetworkGroup.address_builder, value)

    def test_address_is_default(self):
        group = NetworkGroup()
        print group.addresses[0].__class__
        assert_true(group.address_is_default)
        group.add(self.address01)
        assert_false(group.address_is_default)
        group.add(self.address02)
        group.remove(self.address01)
        assert_false(group.address_is_default)
        group.remove(self.address02)
        assert_true(group.address_is_default)

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
        group = NetworkGroup()
        assert_equals(group.__repr__(), "<NetworkGroup 0.0.0.0/0>")
        group.add(self.address01)
        assert_equals(group.__repr__(), "<NetworkGroup 10.0.0.0/8>")
        group.add(self.address02)
        assert_equals(group.__repr__(), "<NetworkGroup [u'10.0.0.0/8', u'192.168.0.0/16']>")

    def test_equality(self):
        group01 = NetworkGroup()
        group02 = NetworkGroup()
        assert_equals(group01, group02)
        group01.add(self.address01)
        group02.add(self.address01)
        assert_equals(group01, group02)

    def test_inequality(self):
        group01 = NetworkGroup()
        group02 = NetworkGroup()
        group01.add(self.address01)
        assert_not_equals(group01, group02)
        group02.add(self.address01)
        assert_not_equals(group01, group02)

    def test_contains(self):
        group = NetworkGroup()
        assert_in('10.0.0.0/8', group)
        group.add(self.address01)
        assert_in('10.0.0.0/8', group)
        assert_not_in('11.0.0.0/8', group)
        assert_not_in('0.0.0.0/0', group)

    def test_contains_invalid(self):
        group = NetworkGroup()
        for value in self.invalid_types:
            assert_raises(TypeError, group.__contains__, value)

    def test_from_string(self):
        group = NetworkGroup.from_string('10.0.0.0/8')
        assert_is_instance(group, NetworkGroup)
