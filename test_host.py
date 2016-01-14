# -*- coding: utf-8 -*-

from netobj.host import Host, HostEntry, HostEntryList

from nose.tools import assert_raises, assert_equals, assert_not_equals, assert_in, assert_not_in


class TestHost(object):
    def test_initilization(self):
        host = Host('test1')
        assert_in('test1', host)

    def test_display_name(self):
        host = Host('test1')
        assert_equals(host.display_name, 'test1')
        assert_raises(ValueError, setattr, host, 'display_name', 'test2')
        host.add('test2')
        assert_equals(host.display_name, 'test1')
        host.display_name = 'test2'
        assert_equals(host.display_name, 'test2')

    def test_str(self):
        host = Host('test1')
        assert_equals(host.__str__(), 'Host test1')

    def test_repr(self):
        host = Host('test1')
        assert_equals(host.__repr__(), '<Host test1>')


class TestHostEntryList(object):
    def test_length(self):
        hosts = HostEntryList()
        hosts.add('test1')
        assert_equals(len(hosts), 1)
        hosts.add('test2')
        assert_equals(len(hosts), 2)
        hosts.add('test1')
        assert_equals(len(hosts), 2)

    def test_itr(self):
        hosts = HostEntryList()
        hosts.add('test1')
        hosts.add('test2')
        host = hosts.next()
        assert_equals(host.name, 'test1')
        host = hosts.next()
        assert_equals(host.name, 'test2')
        assert_raises(StopIteration, hosts.next)
        host = hosts.next()
        assert_equals(host.name, 'test1')
        host = hosts.next()
        assert_equals(host.name, 'test2')
        assert_raises(StopIteration, hosts.next)

    def test_add(self):
        hosts = HostEntryList()
        hosts.add('test1')
        assert_in('test1', hosts)
        assert_not_in('test2', hosts)

    def test_repr(self):
        hosts = HostEntryList()
        hosts.add('1.2.3.4')
        assert_equals(hosts.__repr__(), '<HostList \'1.2.3.4\'>')
        hosts.add('2.3.4.5')
        hosts.add('3.4.5.6')
        hosts.add('4.5.6.7')
        assert_equals(hosts.__repr__(), '<HostList \'1.2.3.4, 2.3.4.5, 3.4.5.6\'>')

    def test_str(self):
        hosts = HostEntryList()
        hosts.add('1.2.3.4')
        assert_equals(hosts.__str__(), 'HostList (1)')
        hosts.add('2.3.4.5')
        hosts.add('3.4.5.6')
        hosts.add('4.5.6.7')
        assert_equals(hosts.__str__(), 'HostList (4)')


class TestHostEntry(object):

    def test_validation_host_length(self):
        name_too_short = ''
        assert_raises(ValueError, HostEntry._validate_name, name_too_short)

        name_too_long = 'x' * 64
        assert_raises(ValueError, HostEntry._validate_name, name_too_long)

    def test_validation_domain_length(self):
        valid_hostname = 'hostname'
        invalid_domain = 'x' * 254
        h = HostEntry(valid_hostname)
        assert_raises(ValueError, setattr, h, 'domain', invalid_domain)

    def test_validation_ip(self):
        h = HostEntry('test', '1.2.3.4')
        assert_raises(TypeError, setattr, h, 'ip', 1)
        assert_raises(ValueError, setattr, h, 'ip', '2.3.4.256')
        assert_raises(ValueError, setattr, h, 'ip', 'sadf')

    def test_initilization_ip(self):
        h = HostEntry('test')
        h.ip = '2.3.4.5'
        assert_equals(h.ip, '2.3.4.5')

    def test_validation_host_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, HostEntry._validate_name, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, HostEntry._validate_name, invalid_character)

    def test_validation_fqdn_character_set(self):
        invalid_encoding = u'høst'
        assert_raises(ValueError, HostEntry._validate_name, invalid_encoding)
        invalid_character = 'h+st'
        assert_raises(ValueError, HostEntry._validate_name, invalid_character)

    def test_initilization(self):
        hostname = 'host1'
        host = HostEntry(hostname)
        assert_equals(host.domain, '')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example'
        host = HostEntry(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example')
        assert_equals(host.fqdn, hostname)
        hostname = 'host1.example.com'
        host = HostEntry(hostname)
        assert_equals(host.name, 'host1')
        assert_equals(host.domain, 'example.com')
        assert_equals(host.fqdn, hostname)

    def test_cleanup_host(self):
        hostname = 'host1.example.com.'
        host = HostEntry(hostname)
        host.name = 'HOSTNAME'
        assert_equals(host.name, 'hostname')

    def test_cleanup_domain(self):
        hostname = 'host1.example.com.'
        host = HostEntry(hostname)
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
        host1 = HostEntry(hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname)
        assert_equals(host1, hostname.upper())
        assert_equals(host1, 'host1'.upper())
        assert_equals(host1, hostname.split('.')[0])
        assert_not_equals(host1, 'example.com')
        assert_not_equals(host1, 'host')

    def test_eqality_ip(self):
        ip = '1.1.1.1'
        host = HostEntry('test', ip=ip)
        assert_equals(host, ip)

    def test_eqality_hosts(self):
        host1 = HostEntry('host1', '1.1.1.1')
        host2 = HostEntry('host1', '1.1.1.1')
        assert_equals(host1, host2)
        host2 = HostEntry('host2', '1.1.1.1')
        assert_equals(host1, host2)
        host2 = HostEntry('host1.example.com', '2.2.2.2')
        assert_equals(host1, host2)
