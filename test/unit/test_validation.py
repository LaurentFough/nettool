# -*- coding: utf-8 -*-

import ipaddress

from nose.tools import assert_true, assert_false, assert_raises
from nettool.nettest import NetTest as nu


class TestValidation(object):

    def setup(self):
        self.wildcards = [ipaddress.IPv4Interface(
            unicode('0.0.0.0/{}'.format(x))).network.hostmask.exploded for x in range(0, 33)]
        self.netmasks = [ipaddress.IPv4Interface(
            unicode('255.255.255.255/{}'.format(x)))
            .network.network_address.exploded for x in range(0, 33)]

    def test_netmask_validation(self):
        for netmask in self.netmasks:
            assert_true(nu.validate.netmask(netmask))
        assert_false(nu.validate.netmask('netmask'))
        assert_false(nu.validate.netmask(33))
        assert_raises(ValueError, nu.validate.netmask, 'not a netmask', True)

    def test_wildcard_validation(self):
        for wildcard in self.wildcards:
            assert_true(nu.validate.wildcard(wildcard))
        assert_false(nu.validate.wildcard('wildcard'))
        assert_false(nu.validate.wildcard(33))
        assert_raises(ValueError, nu.validate.wildcard, 'not a wildcard', True)

    def test_prefix_validation(self):
        for wildcard in self.wildcards:
            assert_true(nu.validate.wildcard(wildcard))
        assert_false(nu.validate.prefix('prefix'))
        assert_false(nu.validate.prefix(33))
        assert_raises(ValueError, nu.validate.prefix, 'not a prefix', True)

    def test_host_validation(self):
        assert_false(nu.validate.host('host.example.com'))
        assert_false(nu.validate.host(''))
        assert_false(nu.validate.host('x' * 64))
        assert_false(nu.validate.host(':'))
        assert_false(nu.validate.host(20))
        assert_true(nu.validate.host('host'))
        assert_raises(TypeError, nu.validate.host, 1, True)
        assert_raises(ValueError, nu.validate.host, 'host.example.com', True)
        assert_raises(ValueError, nu.validate.host, 'h' * 64, True)

    def test_is_subnet(self):
        assert nu.validate.is_subnet('1.2.3.1', '1.2.3.1')
        assert nu.validate.is_subnet('1.2.3.1', '1.2.3.1/24')
        assert nu.validate.is_subnet('1.2.3.1/24', '1.2.3.1/24')
        assert nu.validate.is_subnet('1.2.3.0 255.255.255.0', '1.2.3.1/16')
        assert nu.validate.is_subnet('1.2.3.1/32', '1.2.3.0 0.0.0.255')

        assert not nu.validate.is_subnet('1.2.3.1/24', '1.2.3.1')
        assert not nu.validate.is_subnet('1.2.3.0 0.0.0.255', '1.2.3.1/32')
        assert not nu.validate.is_subnet('1.2.3.1/16', '1.2.3.0 255.255.255.0')

    def test_hostname_validation(self):
        assert_true(nu.validate.hostname('host.example.com'))
        assert_false(nu.validate.hostname(''))
        assert_false(nu.validate.hostname('x' * 64))
        assert_false(nu.validate.hostname(':'))
        assert_false(nu.validate.hostname(20))
        assert_true(nu.validate.hostname('host'))
        assert_raises(TypeError, nu.validate.hostname, 1, True)
        assert_raises(ValueError, nu.validate.hostname, 'x' * 254, True)
        assert_raises(ValueError, nu.validate.hostname, 'ø', True)

    def test_ip_validation(self):
        assert nu.validate.ip('1.2.3.4')
        assert nu.validate.ip('1.2.3.4/32')
        assert nu.validate.ip(u'1.2.3.4')
        assert not nu.validate.ip(u' ')
        assert not nu.validate.ip(u'')
        assert not nu.validate.ip(u'256.2.3.4')
        assert not nu.validate.ip('host')
        assert not nu.validate.ip('')
        assert not nu.validate.ip(1)
        assert_raises(TypeError, nu.validate.ip, 1, True)
        assert_raises(ValueError, nu.validate.ip, '1.2.3.4.5', True)

    def test_network_validation(self):
        assert nu.validate.network('1.2.3.4/32')
        assert nu.validate.network('1.2.3.4/0')
        assert nu.validate.network('1.2.3.4')
        assert nu.validate.network(u'1.2.3.4')
        assert nu.validate.network(u'1.2.3.0 255.255.255.0')
        assert nu.validate.network(u'1.2.3.0 0.0.0.255')
        assert not nu.validate.network(u'256.2.3.4')
        assert not nu.validate.network('host')
        assert not nu.validate.network('')
        assert not nu.validate.network(1)
        assert_raises(TypeError, nu.validate.network, 1, True)
        assert_raises(ValueError, nu.validate.network, 'not a network', True)

    def test_port_validation(self):
        assert_true(nu.validate._port(1))
        assert_true(nu.validate._port(65535))
        assert_true(nu.validate._port('1'))
        assert_false(nu.validate._port('port'))
        assert_false(nu.validate._port(0))
        assert_false(nu.validate._port(65536))
        assert_raises(TypeError, nu.validate._port, 'port', True)
        assert_raises(ValueError, nu.validate._port, 0, True)
        assert_raises(ValueError, nu.validate._port, 65536, True)

    def test_tcp_port_validation(self):
        assert_true(nu.validate.tcp_port(1))
        assert_true(nu.validate.tcp_port(65535))
        assert_true(nu.validate.tcp_port('1'))
        assert_false(nu.validate.tcp_port('port'))
        assert_false(nu.validate.tcp_port(0))
        assert_false(nu.validate.tcp_port(65536))
        assert_raises(TypeError, nu.validate.tcp_port, 'port', True)
        assert_raises(ValueError, nu.validate.tcp_port, 0, True)
        assert_raises(ValueError, nu.validate.tcp_port, 65536, True)

    def test_udp_port_validation(self):
        assert_true(nu.validate.udp_port(1))
        assert_true(nu.validate.udp_port(65535))
        assert_true(nu.validate.udp_port('1'))
        assert_false(nu.validate.udp_port('port'))
        assert_false(nu.validate.udp_port(0))
        assert_false(nu.validate.udp_port(65536))
        assert_raises(TypeError, nu.validate.udp_port, 'port', True)
        assert_raises(ValueError, nu.validate.udp_port, 0, True)
        assert_raises(ValueError, nu.validate.udp_port, 65536, True)
