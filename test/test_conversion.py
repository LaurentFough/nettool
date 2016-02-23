# -*- coding: utf-8 -*-

import ipaddress

from nose.tools import assert_equals, assert_raises

from nettool.nutility import NUtility as nu


class TestConversion(object):

    def setup(self):
        self.netmasks = [ipaddress.IPv4Interface(unicode('255.255.255.255/{0}'.format(x))).network.network_address.exploded for x in range(0, 33)]
        self.wildcards = [ipaddress.IPv4Interface(unicode('0.0.0.0/{0}'.format(x))).network.hostmask.exploded for x in range(0, 33)]

    def test_netmask_to_wildcard_conversion(self):
        for index, netmask in enumerate(self.netmasks):
            assert_equals(nu.convert.netmask.wildcard(netmask), self.wildcards[index])

    def test_netmask_to_prefix_conversion(self):
        for index, netmask in enumerate(self.netmasks):
            assert_equals(nu.convert.netmask.prefix(netmask), index)

    def test_wildcard_to_netmask_conversion(self):
        for index, wildcard in enumerate(self.wildcards):
            assert_equals(nu.convert.wildcard.netmask(wildcard), self.netmasks[index])

    def test_wildcard_to_prefix_conversion(self):
        for index, wildcard in enumerate(self.wildcards):
            assert_equals(nu.convert.wildcard.prefix(wildcard), index)

    def test_prefix_to_netmask_conversion(self):
        for prefix in range(0, 33):
            assert_equals(nu.convert.prefix.netmask(prefix), self.netmasks[prefix])

    def test_prefix_to_wildcard_conversion(self):
        for prefix in range(0, 33):
            assert_equals(nu.convert.prefix.wildcard(prefix), self.wildcards[prefix])

    def test_netmask_to_wildcard_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.netmask.wildcard, 1)

    def test_netmask_to_prefix_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.netmask.prefix, 1)

    def test_wildcard_to_netmask_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.wildcard.netmask, 1)

    def test_wildcard_to_prefix_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.wildcard.prefix, 1)

    def test_prefix_to_netmask_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.prefix.netmask, 'invalid')

    def test_prefix_to_wildcard_conversion_invalid_input(self):
        assert_raises(ValueError, nu.convert.prefix.wildcard, 'invalid')

    def test_coerce_string_to_hostname(self):
        assert_equals(nu.coerce.string.hostname('host name.example.com'), 'host-name.example.com')
        assert_equals(nu.coerce.string.hostname('(host)name.example.com'), 'host-name.example.com')
        assert_equals(nu.coerce.string.hostname('HOSTNAME.EXAMPLE.COM'), 'hostname.example.com')
        assert_equals(nu.coerce.string.hostname('-hostname.example.com.'), 'hostname.example.com')
        assert_equals(nu.coerce.string.hostname('host_name.example.com'), 'host-name.example.com')
        assert_equals(nu.coerce.string.hostname(' hostname.example.com '), 'hostname.example.com')
        assert_equals(nu.coerce.string.hostname(' hostname(a)-1.example.com '), 'hostname-a-1.example.com')
        assert_equals(nu.coerce.string.hostname(u'ø.example.com'), 'o.example.com')
        assert_equals(nu.coerce.string.hostname(u'å.example.com'), 'a.example.com')
        assert_equals(nu.coerce.string.hostname('host/a.example.com'), 'host-a.example.com')
        assert_equals(nu.coerce.string.hostname('host\\a.example.com'), 'host-a.example.com')
        assert_equals(nu.coerce.string.hostname('host:a.example.com'), 'host-a.example.com')

    def test_coerce_string_to_host(self):
        assert_equals(nu.coerce.string.hostname('host name'), 'host-name')
        assert_equals(nu.coerce.string.hostname('(host)name'), 'host-name')
        assert_equals(nu.coerce.string.hostname('HOSTNAME'), 'hostname')
        assert_equals(nu.coerce.string.hostname('-hostname.'), 'hostname')
        assert_equals(nu.coerce.string.hostname('host_name'), 'host-name')
        assert_equals(nu.coerce.string.hostname(' hostname '), 'hostname')
        assert_equals(nu.coerce.string.hostname(u'ø'), 'o')
        assert_equals(nu.coerce.string.hostname(u'å'), 'a')
