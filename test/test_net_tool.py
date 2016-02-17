# -*- coding: utf-8 -*-

import ipaddress

from nose.tools import assert_equals, assert_raises

from netobj.nutility import NUtility


class TestNetTool(object):

    def setup(self):
        self.netmasks = [ipaddress.IPv4Interface(unicode('255.255.255.255/{0}'.format(x))).network.network_address.exploded for x in range(0, 33)]
        self.wildcards = [ipaddress.IPv4Interface(unicode('0.0.0.0/{0}'.format(x))).network.hostmask.exploded for x in range(0, 33)]

    def test_wildcard_to_netmask_conversion_invalid_input(self):
        assert_raises(ValueError, NUtility.convert.netmask.wildcard, 1)

    def test_wildcard_to_netmask_conversion(self):
        assert_equals(NUtility.convert.netmask.wildcard('255.255.0.0'), '0.0.255.255')
        for index, netmask in enumerate(self.netmasks):
            assert_equals(NUtility.convert.netmask.wildcard(netmask), self.wildcards[index])

    def test_netmask_to_wildcard_conversion(self):
        assert_equals(NUtility.convert.wildcard.netmask('0.0.255.255'), '255.255.0.0')
        for index, wildcard in enumerate(self.wildcards):
            assert_equals(NUtility.convert.wildcard.netmask(wildcard), self.netmasks[index])
