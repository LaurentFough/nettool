# -*- coding: utf-8 -*-

from netobj.validate import Validate
from netobj.host import Host, HostEntry, HostEntryList

from nose.tools import assert_raises, assert_equals, assert_not_equals, assert_in, assert_not_in, assert_true, assert_false


class TestHost(object):
    def test_initilization(self):
        host = Host('test1')
        assert_in('test1', host)

    def test_display_name(self):
        host = Host('test1')
        assert_equals(host.display_name, 'test1')
        host._add('test2')
        # assert_equals(host.display_name, 'test1')
        # host.display_name = 'test2'
        # assert_equals(host.display_name, 'test2')

    def test_display_name_update(self):
        host = Host('test1')
        assert_equals(host.display_name, 'test1')
        host.add('test1.example.com')
        # host.add(HostEntry('test1.example.com'))
        assert_equals(host.display_name, 'test1.example.com')

    def test_add(self):
        host = Host('test1')
        assert_equals(len(host), 1)
        host = Host(HostEntry('test1'))
        host_entry_1 = HostEntry('test1')
        assert_equals(len(host), 1)
        host.add(host_entry_1)
        assert_equals(len(host), 1)

    def test_add_failure(self):
        host = Host(HostEntry('test1'))
        assert_raises(TypeError, host.add, list())
        # Different host, add fails
        host_entry_2 = HostEntry('test2')
        assert_raises(ValueError, host.add, host_entry_2)

    def test_add_fqdn_to_shortname(self):
        # New fqdn updates the domain if exisiting domain is empty
        host = Host(HostEntry('test1'))
        assert_equals(host[0].fqdn, 'test1')
        host_entry_2 = HostEntry('test1.example.com')
        host.add(host_entry_2)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_2.fqdn)

    def test_add_ip_to_no_ip_host(self):
        # New IP with matching hostnames updates existing hostentry's ip
        host_entry_1 = HostEntry('test1.example.com')
        host = Host(host_entry_1)
        host_entry_2 = HostEntry('test1', '1.2.3.4')
        host.add(host_entry_2)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_1.fqdn)
        assert_equals(host[0].ip, host_entry_2.ip)
        host[0].ip = None
        host_entry_3 = HostEntry('test1.example.com', '1.2.3.4')
        host.add(host_entry_3)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_3.fqdn)
        assert_equals(host[0].ip, host_entry_3.ip)

    def test_add_new_host_existing_ip(self):
        # New Hostname with duplicate ip adds new host entry
        host = Host(HostEntry('test1', '1.2.3.4'))
        host_entry_3 = HostEntry('test2', '1.2.3.4')
        host.add(host_entry_3)
        assert_equals(len(host), 2)
        assert_equals(host[-1].fqdn, host_entry_3.fqdn)
        del host[-1]
        assert_equals(len(host), 1)
        host_entry_4 = HostEntry('test2.example.com', '1.2.3.4')
        host.add(host_entry_4)
        assert_equals(len(host), 2)
        assert_equals(host[-1].fqdn, host_entry_4.fqdn)

    def test_add_new_ip_existing_name(self):
        # New Hostname with duplicate ip adds new host entry
        host = Host(HostEntry('test1', '1.2.3.4'))
        host.add(HostEntry('test1', '2.3.4.5'))
        assert_equals(len(host), 2)
        assert_equals(host[0].fqdn, 'test1')
        assert_equals(host[1].fqdn, 'test1')
        assert_equals(host[0].ip, '1.2.3.4')
        assert_equals(host[1].ip, '2.3.4.5')
        del host[-1]
        host.add(HostEntry('test1.example.com', '2.3.4.5'))
        assert_equals(len(host), 2)
        assert_equals(host[0].fqdn, 'test1.example.com')
        assert_equals(host[1].fqdn, 'test1.example.com')
        assert_equals(host[0].ip, '1.2.3.4')
        assert_equals(host[1].ip, '2.3.4.5')

    def test_equals(self):
        """ Hosts are equal if there is one overlapping entry """
        host = Host(HostEntry('test', '1.2.3.4'))
        assert_true('test' in host)
        assert_true(HostEntry('test') in host)
        assert_true(HostEntry('test', '1.2.3.4') in host)
        assert_true(HostEntry('test.example.com') in host)
        assert_true(HostEntry('test.example.com', '1.2.3.4') in host)

        assert_false('test1' in host)
        assert_false(HostEntry('test1') in host)
        assert_false(HostEntry('test1', '2.3.4.5') in host)
        assert_false(HostEntry('test1.example.com') in host)
        assert_false(HostEntry('test1.example.com', '2.3.4.5') in host)

    def test_str(self):
        host = Host('test1')
        assert_equals(host.__str__(), 'Host test1')

    def test_repr(self):
        host = Host('test1')
        assert_equals(host.__repr__(), '<Host test1>')


class TestHostEntryList(object):
    def test_indexing(self):
        hosts = HostEntryList()
        hosts.add('test1')
        assert_equals(hosts[0].name, 'test1')
        hosts.add('test2')
        assert_equals(hosts[1].name, 'test2')
        assert_equals(hosts[-1].name, 'test2')

    def test_deletion(self):
        hosts = HostEntryList()
        hosts.add('test1')
        assert_equals(len(hosts), 1)
        hosts.add('test2')
        assert_equals(len(hosts), 2)
        del hosts[-1]
        assert_equals(len(hosts), 1)

    def test_length(self):
        hosts = HostEntryList()
        hosts.add('test1')
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

    def test_get(self):
        hosts = HostEntryList()
        hosts.add('test')
        assert_equals(hosts.get('test'), HostEntry('test'))
        assert_equals(hosts.get('test'), HostEntry('test'))
        assert_equals(hosts.get('test'), HostEntry('test'))
        assert_equals(hosts.get('test1'), None)
        hosts.add('test.example.com')
        assert_equals(hosts.get('test'), HostEntry('test'))
        assert_equals(hosts.get('test.example.com'), HostEntry('test'))
        assert_equals(hosts.get('test'), HostEntry('test.example.com'))
        assert_equals(hosts.get('test.example.com'), HostEntry('test.example.com'))

    def test_contains(self):
        host = HostEntryList()
        host.add(HostEntry('test', '1.2.3.4'))
        assert_true('test' in host)
        assert_true(HostEntry('test') in host)
        assert_true(HostEntry('test', '1.2.3.4') in host)
        assert_true(HostEntry('test.example.com') in host)
        assert_true(HostEntry('test.example.com', '1.2.3.4') in host)

        assert_false('test1' in host)
        assert_false(HostEntry('test1') in host)
        assert_false(HostEntry('test1', '2.3.4.5') in host)
        assert_false(HostEntry('test1.example.com') in host)
        assert_false(HostEntry('test1.example.com', '2.3.4.5') in host)

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

    def test_initilization_ip(self):
        h = HostEntry('test')
        h.ip = '2.3.4.5'
        assert_equals(h.ip, '2.3.4.5')

    def test_validation_host_length(self):
        name_too_short = ''
        assert_raises(ValueError, Validate.host, name_too_short)

        name_too_long = 'x' * 64
        assert_raises(ValueError, Validate.host, name_too_long)

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

        # No IPs specified
        host1 = HostEntry('test1')
        host2 = HostEntry('test2')
        assert_not_equals(host1, host2)

    def test_eqality_ip(self):
        ip = '1.1.1.1'
        host = HostEntry('test', ip=ip)
        assert_equals(host, ip)

    def test_eqality_hosts(self):
        # Total match
        host1 = HostEntry('host1', '1.1.1.1')
        host2 = HostEntry('host1', '1.1.1.1')
        assert_equals(host1, host2)

        # Hostname match
        host3 = HostEntry('host1', '2.2.2.2')
        assert_equals(host1, host3)
        host3 = HostEntry('host1')
        assert_equals(host1, host3)

        # Name in FQDN match
        host4 = HostEntry('host1.example.com', '3.3.3.3')
        assert_equals(host1, host4)
        host4 = HostEntry('host1.example.com')
        assert_equals(host1, host4)

        # FQDN match
        host5 = HostEntry('host1.example.com', '4.4.4.4')
        assert_equals(host4, host5)
        host5 = HostEntry('host1.example.com')
        assert_equals(host4, host5)

        # IP match
        host6 = HostEntry('host2', '1.1.1.1')
        assert_equals(host1, host6)

    def test_ineqality_hosts(self):
        host1 = HostEntry('host1', '1.1.1.1')
        host2 = HostEntry('host2', '2.2.2.2')
        assert_not_equals(host1, host2)

        host1 = HostEntry('host1', '1.1.1.1')
        host2 = HostEntry('host', '2.2.2.2')
        assert_not_equals(host1, host2)
