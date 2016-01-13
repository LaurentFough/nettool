# -*- coding: utf-8 -*-

from main import Host

from nose.tools import assert_raises, assert_equals, assert_not_equals


class TestHost(object):

    def test_validation_host_length(self):
        name_too_short = ''
        assert_raises(ValueError, Host._validate_name, name_too_short)

        name_too_long = 'x' * 64
        assert_raises(ValueError, Host._validate_name, name_too_long)

    def test_validation_domain_length(self):
        valid_hostname = 'hostname'
        invalid_domain = 'x' * 254
        h = Host(valid_hostname)
        assert_raises(ValueError, setattr, h, 'domain', invalid_domain)

    def test_validation_ip(self):
        h = Host('test', '1.2.3.4')
        assert_raises(TypeError, setattr, h, 'ip', 1)
        assert_raises(ValueError, setattr, h, 'ip', '2.3.4.256')
        assert_raises(ValueError, setattr, h, 'ip', 'sadf')

    def test_initilization_ip(self):
        h = Host('test')
        h.ip = '2.3.4.5'
        assert_equals(h.ip, '2.3.4.5')

    def test_validation_host_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, Host._validate_name, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, Host._validate_name, invalid_character)

    def test_validation_fqdn_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, Host._validate_name, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, Host._validate_name, invalid_character)

    def test_initilization(self):
        hostname = 'host1'
        host = Host(hostname)
        assert_equals(host.domain, '')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example'
        host = Host(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example.com'
        host = Host(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example.com')
        assert_equals(host.fqdn, hostname)

    def test_cleanup_host(self):
        hostname = 'host1.example.com.'
        host = Host(hostname)
        host.name = 'HOSTNAME'
        assert_equals(host.name, 'hostname')

    def test_cleanup_domain(self):
        hostname = 'host1.example.com.'
        host = Host(hostname)
        domain = 'example.com'
        assert_equals(host.domain, 'example.com')
        host.domain = '.example.com'
        assert_equals(host.domain, domain)
        host.domain = 'example.com.'
        assert_equals(host.domain, domain)
        host.domain = '.example.com.'
        assert_equals(host.domain, domain)
        host.domain = 'EXAMPLE.COM'
        assert_equals(host.domain, domain)

    def test_eqality_name(self):
        hostname = 'host1.example.com'
        host1 = Host(hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname.upper())
        assert_equals(host1, 'host1'.upper())
        assert_equals(host1, hostname.split('.')[0])
        assert_not_equals(host1, 'example.com')
        assert_not_equals(host1, 'host')

    def test_eqality_ip(self):
        ip = '1.1.1.1'
        host = Host('test', ip=ip)
        assert_equals(host, ip)

    def test_eqality_hosts(self):
        host1 = Host('host1', '1.1.1.1')
        host2 = Host('host1', '1.1.1.1')
        assert_equals(host1, host2)
        host2 = Host('host2', '1.1.1.1')
        assert_equals(host1, host2)
        host2 = Host('host1.example.com', '2.2.2.2')
        assert_equals(host1, host2)
