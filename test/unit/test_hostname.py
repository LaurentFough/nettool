# -*- coding: utf-8 -*-

from nettool.host import Hostname

from nose.tools import assert_raises, assert_equals, assert_not_equals


class TestHostname(object):

    def test_initilization(self):
        assert Hostname(name='test', ip=None).ip is None
        assert Hostname(name='test', ip='').ip is None
        assert Hostname(name='test', ip=' ').ip is None
        hostname = 'host1'
        host = Hostname(hostname)
        assert host.domain == ''
        assert host.fqdn == hostname
        hostname = 'host1.example'
        host = Hostname(hostname)
        assert host.name == 'host1'
        assert host.domain == 'example'
        assert host.fqdn == hostname
        hostname = 'host1.example.com'
        host = Hostname(hostname)
        assert host.name == 'host1'
        assert host.domain == 'example.com'
        assert host.fqdn == hostname
        assert Hostname('test', '2.3.4.5').ip == '2.3.4.5'
        assert Hostname('test', '2.3.4.5').routing_domain is None
        assert Hostname('test', '2.3.4.5', 'rd01').routing_domain == 'rd01'

    def test_initilization_invalid(self):
        assert_raises(ValueError, Hostname, None, None)
        assert_raises(ValueError, Hostname, '1.2.3.4', '2.3.4.5')

    def test_validation_domain_length(self):
        valid_hostname = 'hostname'
        invalid_domain = 'x' * 254
        h = Hostname(valid_hostname)
        assert_raises(ValueError, setattr, h, 'domain', invalid_domain)

    def test_str(self):
        assert_equals(str(Hostname(name=None, ip='1.2.3.4')), '1.2.3.4')
        assert_equals(str(Hostname(name='hostname', ip='1.2.3.4')), 'hostname 1.2.3.4')
        assert_equals(str(Hostname(name='hostname.example.com', ip='1.2.3.4')),
                      'hostname.example.com 1.2.3.4')
        assert_equals(str(Hostname(name='hostname.example.com')), 'hostname.example.com')

    def test_validation_ip(self):
        h = Hostname('test', '1.2.3.4')
        assert_raises(TypeError, setattr, h, 'ip', 1)
        assert_raises(ValueError, setattr, h, 'ip', '2.3.4.256')
        assert_raises(ValueError, setattr, h, 'ip', 'sadf')

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
        assert host1 == hostname
        assert host1 == hostname
        assert host1 == hostname.upper()
        assert host1 == 'host1'.upper()
        assert host1 == hostname.split('.')[0]
        assert host1 != 'example.com'
        assert host1 != 'host'

        # No IPs specified
        host1 = Hostname('test1')
        host2 = Hostname('test2')
        assert_not_equals(host1, host2)

    def test_eqality_ip(self):
        ip = '1.1.1.1'
        host = Hostname('test', ip=ip)
        assert_equals(host, ip)

    def test_eqality_routing_domain(self):
        hostname = 'test'
        ip = '1.1.1.1'
        rd01 = 'test_routing_domain'
        rd02 = 'TEST_ROUTING_DOMAIN'
        rd03 = 'TEST_ROUTING_DOMAIN01'
        assert Hostname(hostname, ip=ip, routing_domain=rd01) \
            == Hostname(hostname, ip=ip, routing_domain=rd02)
        assert Hostname(hostname, ip=ip, routing_domain=rd01) \
            != Hostname(hostname, ip=ip, routing_domain=rd03)

    def test_equality_hostnames(self):
        # Total match
        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host1', '1.1.1.1')
        assert host1 == host2

        # Non-fqdn hostname to fqdn hostname match
        assert Hostname('host.example.com', '1.1.1.1') == Hostname('host', '1.1.1.1')
        assert Hostname('host.example.com', '1.1.1.1') == Hostname('host', '1.1.1.2')

        # Hostname match
        host3 = Hostname('host1', '2.2.2.2')
        assert host1 == host3
        host3 = Hostname('host1')
        assert host1 == host3

        # Name in FQDN match
        host4 = Hostname('host1.example.com', '3.3.3.3')
        assert host1 == host4
        host4 = Hostname('host1.example.com')
        assert host1 == host4

        # FQDN match
        host5 = Hostname('host1.example.com', '4.4.4.4')
        assert host4 == host5
        host5 = Hostname('host1.example.com')
        assert host4 == host5

        # IP match
        assert Hostname('host1', '1.1.1.1') == Hostname('host2', '1.1.1.1')

        # Routing Domain
        assert Hostname('host1', '1.1.1.1', routing_domain='1') == \
            Hostname('host2', '1.1.1.1', routing_domain='1')

    def test_ineqality_hosts(self):
        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host2', '2.2.2.2')
        assert_not_equals(host1, host2)

        host1 = Hostname('host1.example.com')
        host2 = Hostname('host1.contoso.com')
        assert host1 != host2

        host1 = Hostname('host1', '1.1.1.1')
        host2 = Hostname('host', '2.2.2.2')
        assert host1 != host2

        host1 = Hostname('host1', '1.1.1.1', routing_domain='1')
        host1 = Hostname('host1', '1.1.1.1', routing_domain='2')
        assert host1 != host2

    def test_name_setter(self):
        test_hostname = 'host.test.com'
        update_hostname = 'host.example.com'
        hostname = Hostname(test_hostname)
        assert_equals(hostname.fqdn, test_hostname)
        hostname.name = update_hostname
        assert_equals(hostname.fqdn, update_hostname)
