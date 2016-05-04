# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface as IPv4Int

from nose.tools import assert_equals, assert_raises

from nettool.nettest import NetTest as nu


class TestConversion(object):

    def setup(self):
        self.netmasks = list()
        self.wildcards = list()
        for x in range(0, 33):
            netmask = IPv4Int(u'255.255.255.255/{0}'.format(x)).network.network_address.exploded
            self.netmasks.append(netmask)
            wildcard = IPv4Int(u'0.0.0.0/{0}'.format(x)).network.hostmask.exploded
            self.wildcards.append(wildcard)

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

    def test_convert_string_to_cidr(self):
        assert nu.convert.string.cidr('1.2.3.1/24') == '1.2.3.0/24'
        assert nu.convert.string.cidr('1.2.3.0 255.255.255.0') == '1.2.3.0/24'
        assert nu.convert.string.cidr('1.2.3.0 255.255.255.255') == '1.2.3.0/32'
        assert nu.convert.string.cidr('1.2.3.0 0.0.0.255') == '1.2.3.0/24'

    def test_convert_string_to_ip(self):
        assert nu.convert.string.ip('1.2.3.1/24') == '1.2.3.1'
        assert nu.convert.string.ip('1.2.3.0 255.255.255.0') == '1.2.3.0'
        assert nu.convert.string.ip('1.2.3.0 255.255.255.255') == '1.2.3.0'
        assert nu.convert.string.ip('1.2.3.0 0.0.0.255') == '1.2.3.0'

    def test_convert_string_to_hostname(self):
        assert_equals(nu.convert.string.hostname('host name.example.com'), 'host-name.example.com')
        assert_equals(nu.convert.string.hostname('(host)name.example.com'), 'host-name.example.com')
        assert_equals(nu.convert.string.hostname('HOSTNAME.EXAMPLE.COM'), 'hostname.example.com')
        assert_equals(nu.convert.string.hostname('-hostname.example.com.'), 'hostname.example.com')
        assert_equals(nu.convert.string.hostname('host_name.example.com'), 'host-name.example.com')
        assert_equals(nu.convert.string.hostname(' hostname.example.com '), 'hostname.example.com')
        hostname = nu.convert.string.hostname(' hostname(a)-1.example.com ')
        assert_equals(hostname, 'hostname-a-1.example.com')
        assert_equals(nu.convert.string.hostname(u'ø.example.com'), 'o.example.com')
        assert_equals(nu.convert.string.hostname(u'å.example.com'), 'a.example.com')
        assert_equals(nu.convert.string.hostname('host/a.example.com'), 'host-a.example.com')
        assert_equals(nu.convert.string.hostname('host\\a.example.com'), 'host-a.example.com')
        assert_equals(nu.convert.string.hostname('host:a.example.com'), 'host-a.example.com')

    def test_convert_string_to_host(self):
        assert_equals(nu.convert.string.hostname('host name'), 'host-name')
        assert_equals(nu.convert.string.hostname('(host)name'), 'host-name')
        assert_equals(nu.convert.string.hostname('HOSTNAME'), 'hostname')
        assert_equals(nu.convert.string.hostname('-hostname.'), 'hostname')
        assert_equals(nu.convert.string.hostname('host_name'), 'host-name')
        assert_equals(nu.convert.string.hostname(' hostname '), 'hostname')
        assert_equals(nu.convert.string.hostname(u'ø'), 'o')
        assert_equals(nu.convert.string.hostname(u'å'), 'a')
