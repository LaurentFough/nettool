# -*- coding: utf-8 -*-

from nettool.validate import Validate
from nettool.host import Hostname

from nose.tools import assert_raises, assert_equals, assert_not_equals, assert_true


class TestHostname(object):

    def test_initilization(self):
        assert_equals(Hostname(name='test', ip=None).ip, None)
        assert_equals(Hostname(name='test', ip='').ip, None)
        assert_equals(Hostname(name='test', ip=' ').ip, None)
        hostname = 'host1'
        host = Hostname(hostname)
        assert_equals(host.domain, '')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example'
        host = Hostname(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example.com'
        host = Hostname(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example.com')
        assert_equals(host.fqdn, hostname)
        assert_equals(Hostname('test', '2.3.4.5').ip, '2.3.4.5')

    def test_initilization_invalid(self):
        assert_raises(ValueError, Hostname, '1.2.3.4', '2.3.4.5')

    def test_validation_host_length(self):
        name_too_short = ''
        assert_raises(ValueError, Validate.host, name_too_short)

        name_too_long = 'x' * 64
        assert_raises(ValueError, Validate.host, name_too_long)

    def test_validation_domain_length(self):
        valid_hostname = 'hostname'
        invalid_domain = 'x' * 254
        h = Hostname(valid_hostname)
        assert_raises(ValueError, setattr, h, 'domain', invalid_domain)

    def test_str(self):
        assert_equals(str(Hostname(name=None, ip='1.2.3.4')), '1.2.3.4')
        assert_equals(str(Hostname(name='hostname', ip='1.2.3.4')), 'hostname 1.2.3.4')
        assert_equals(str(Hostname(name='hostname.example.com', ip='1.2.3.4')), 'hostname.example.com 1.2.3.4')

    def test_validation_ip(self):
        h = Hostname('test', '1.2.3.4')
        assert_raises(TypeError, setattr, h, 'ip', 1)
        assert_raises(ValueError, setattr, h, 'ip', '2.3.4.256')
        assert_raises(ValueError, setattr, h, 'ip', 'sadf')

    def test_validation_host_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, Validate.host, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, Validate.host, invalid_character)

    def test_validation_fqdn_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, Validate.host, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, Validate.host, invalid_character)

    def test_cleanup_host(self):
        hostname = 'host1.example.com.'
        host = Hostname(hostname)
        host.name = 'HOSTNAME'
        assert_equals(host.name, 'hostname')

    def test_cleanup_domain(self):
        hostname = 'host1.example.com.'
        host = Hostname(hostname)
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
        host1 = Hostname(hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname.upper())
        assert_equals(host1, 'host1'.upper())
        assert_equals(host1, hostname.split('.')[0])
        assert_not_equals(host1, 'example.com')
        assert_not_equals(host1, 'host')

        # No IPs specified
        host1 = Hostname('test1')
        host2 = Hostname('test2')
        assert_not_equals(host1, host2)

    def test_eqality_ip(self):
        ip = '1.1.1.1'
        host = Hostname('test', ip=ip)
        assert_equals(host, ip)

    def test_equality_hostnames(self):
        # Total match
        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host1', '1.1.1.1')
        assert_equals(host1, host2)

        # Non-fqdn hostname to fqdn hostname match
        assert_equals(Hostname('host.example.com', '1.1.1.1'), Hostname('host', '1.1.1.1'))
        assert_equals(Hostname('host.example.com', '1.1.1.1'), Hostname('host', '1.1.1.2'))

        # Hostname match
        host3 = Hostname('host1', '2.2.2.2')
        assert_equals(host1, host3)
        host3 = Hostname('host1')
        assert_equals(host1, host3)

        # Name in FQDN match
        host4 = Hostname('host1.example.com', '3.3.3.3')
        assert_equals(host1, host4)
        host4 = Hostname('host1.example.com')
        assert_equals(host1, host4)

        # FQDN match
        host5 = Hostname('host1.example.com', '4.4.4.4')
        assert_equals(host4, host5)
        host5 = Hostname('host1.example.com')
        assert_equals(host4, host5)

        # IP match
        assert_equals(Hostname('host1', '1.1.1.1'), Hostname('host2', '1.1.1.1'))

    def test_ineqality_hosts(self):
        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host2', '2.2.2.2')
        assert_not_equals(host1, host2)

        host1 = Hostname('host1.example.com')
        host2 = Hostname('host1.contoso.com')
        assert_not_equals(host1, host2)

        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host', '2.2.2.2')
        assert_not_equals(host1, host2)
