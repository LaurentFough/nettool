# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from nettool.address.address_group import AddressGroup


class TestAddressGroup(object):

    def setup(self):
        self.invalid_types = (True, False, 1)

    def test_initialization_defaults(self):
        group = AddressGroup()
        assert_equals(group.name, AddressGroup._default_name)

    def test_initialization(self):
        group = AddressGroup(name='custom')
        assert_equals(group.name, 'custom')

    def test_initialization_invalid(self):
        for value in self.invalid_types:
            assert_raises(TypeError, AddressGroup, value)

    def test_name_setter(self):
        group = AddressGroup()
        for value in ('test01', 'test02', ):
            group.name = value
            assert_equals(group.name, value)

    def test_name_setter_invalid(self):
        group = AddressGroup()
        for value in self.invalid_types:
            assert_raises(TypeError, setattr, group, 'name', value)

    def test_addresses_getter(self):
        group = AddressGroup()
        assert_equals(group.addresses, [AddressGroup._default_address])
