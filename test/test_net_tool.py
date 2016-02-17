# -*- coding: utf-8 -*-

import ipaddress

from nose.tools import assert_equals, assert_raises, assert_true, assert_false

from netobj.nutility import NUtility


class TestNetTool(object):

    def setup(self):
        self.netmasks = [ipaddress.IPv4Interface(unicode('255.255.255.255/{0}'.format(x))).network.network_address.exploded for x in range(0, 33)]
        self.wildcards = [ipaddress.IPv4Interface(unicode('0.0.0.0/{0}'.format(x))).network.hostmask.exploded for x in range(0, 33)]

    def test_netmask_validation(self):
        for netmask in self.netmasks:
            assert_true(NUtility.validate.netmask(netmask))
        assert_false(NUtility.validate.netmask('netmask'))
        assert_false(NUtility.validate.netmask(33))

    def test_wildcard_validation(self):
        for wildcard in self.wildcards:
            assert_true(NUtility.validate.wildcard(wildcard))
        assert_false(NUtility.validate.wildcard('wildcard'))
        assert_false(NUtility.validate.wildcard(33))

    def test_prefix_validation(self):
        for wildcard in self.wildcards:
            assert_true(NUtility.validate.wildcard(wildcard))
        assert_false(NUtility.validate.wildcard('wildcard'))
        assert_false(NUtility.validate.wildcard(33))

    def test_netmask_to_wildcard_conversion(self):
        for index, netmask in enumerate(self.netmasks):
            assert_equals(NUtility.convert.netmask.wildcard(netmask), self.wildcards[index])

    def test_netmask_to_prefix_conversion(self):
        for index, netmask in enumerate(self.netmasks):
            assert_equals(NUtility.convert.netmask.prefix(netmask), index)

    def test_wildcard_to_netmask_conversion(self):
        for index, wildcard in enumerate(self.wildcards):
            assert_equals(NUtility.convert.wildcard.netmask(wildcard), self.netmasks[index])

    def test_wildcard_to_prefix_conversion(self):
        for index, wildcard in enumerate(self.wildcards):
            assert_equals(NUtility.convert.wildcard.prefix(wildcard), index)

    def test_prefix_to_netmask_conversion(self):
        for prefix in range(0, 33):
            assert_equals(NUtility.convert.prefix.netmask(prefix), self.netmasks[prefix])

    def test_prefix_to_wildcard_conversion(self):
        for prefix in range(0, 33):
            assert_equals(NUtility.convert.prefix.wildcard(prefix), self.wildcards[prefix])

    def test_netmask_to_wildcard_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.netmask.wildcard, 1)

    def test_netmask_to_prefix_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.netmask.prefix, 1)

    def test_wildcard_to_netmask_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.wildcard.netmask, 1)

    def test_wildcard_to_prefix_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.wildcard.prefix, 1)

    def test_prefix_to_netmask_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.prefix.netmask, 'invalid')

    def test_prefix_to_wildcard_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.prefix.wildcard, 'invalid')
