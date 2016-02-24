# -*- coding: utf-8 -*-

from nettool.host import Host, Hostname, HostnameList

from nose.tools import assert_raises, assert_equals, assert_in, assert_not_in, assert_true, assert_false


class TestHost(object):
    def test_initilization(self):
        host = Host('test1')
        assert_in('test1', host)

    def test_display_name(self):
        host = Host('test1')
        assert_equals(host.display_name, 'test1')
        host._add('test2')
        assert_equals(host.display_name, 'test1')
        host.display_name = 'test2'
        assert_equals(host.display_name, 'test2')

    def test_display_name_update(self):
        host = Host('test1')
        assert_equals(host.display_name, 'test1')
        host.add('test1.example.com')
        assert_equals(host.display_name, 'test1.example.com')

    def test_add(self):
        host = Host('test1')
        assert_equals(len(host), 1)
        host = Host(Hostname('test1'))
        host_entry_1 = Hostname('test1')
        assert_equals(len(host), 1)
        host.add(host_entry_1)
        assert_equals(len(host), 1)

    def test_add_failure(self):
        host = Host(Hostname('test1'))
        assert_raises(TypeError, host.add, list())
        # Different host, add fails
        host_entry_2 = Hostname('test2')
        assert_raises(ValueError, host.add, host_entry_2)

    def test_add_fqdn_to_shortname(self):
        # New fqdn updates the domain if exisiting domain is empty
        host = Host(Hostname('test1'))
        assert_equals(host[0].fqdn, 'test1')
        host_entry_2 = Hostname('test1.example.com')
        host.add(host_entry_2)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_2.fqdn)

    def test_add_ip_to_no_ip_host(self):
        # New IP with matching hostnames updates existing hostname's ip
        host_entry_1 = Hostname('test1.example.com')
        host = Host(host_entry_1)
        host_entry_2 = Hostname('test1', '1.2.3.4')
        host.add(host_entry_2)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_1.fqdn)
        assert_equals(host[0].ip, host_entry_2.ip)
        host[0].ip = None
        host_entry_3 = Hostname('test1.example.com', '1.2.3.4')
        host.add(host_entry_3)
        assert_equals(len(host), 1)
        assert_equals(host[0].fqdn, host_entry_3.fqdn)
        assert_equals(host[0].ip, host_entry_3.ip)

    def test_add_new_host_existing_ip(self):
        # New Hostname with duplicate ip adds new host entry
        host = Host(Hostname('test1', '1.2.3.4'))
        host_entry_3 = Hostname('test2', '1.2.3.4')
        host.add(host_entry_3)
        assert_equals(len(host), 2)
        assert_equals(host[-1].fqdn, host_entry_3.fqdn)
        del host[-1]
        assert_equals(len(host), 1)
        host_entry_4 = Hostname('test2.example.com', '1.2.3.4')
        host.add(host_entry_4)
        assert_equals(len(host), 2)
        assert_equals(host[-1].fqdn, host_entry_4.fqdn)

    def test_add_new_ip_existing_name(self):
        # New Hostname with duplicate ip adds new host entry
        host = Host(Hostname('test1', '1.2.3.4'))
        host.add(Hostname('test1', '2.3.4.5'))
        assert_equals(len(host), 2)
        assert_equals(host[0].fqdn, 'test1')
        assert_equals(host[1].fqdn, 'test1')
        assert_equals(host[0].ip, '1.2.3.4')
        assert_equals(host[1].ip, '2.3.4.5')
        del host[-1]
        host.add(Hostname('test1.example.com', '2.3.4.5'))
        assert_equals(len(host), 2)
        assert_equals(host[0].fqdn, 'test1.example.com')
        assert_equals(host[1].fqdn, 'test1.example.com')
        assert_equals(host[0].ip, '1.2.3.4')
        assert_equals(host[1].ip, '2.3.4.5')

    def test_equals(self):
        """ Hosts are equal if there is one overlapping entry """
        host = Host(Hostname('test', '1.2.3.4'))
        assert_true('test' in host)
        assert_true(Hostname('test') in host)
        assert_true(Hostname('test', '1.2.3.4') in host)
        assert_true(Hostname('test.example.com') in host)
        assert_true(Hostname('test.example.com', '1.2.3.4') in host)

        assert_false('test1' in host)
        assert_false(Hostname('test1') in host)
        assert_false(Hostname('test1', '2.3.4.5') in host)
        assert_false(Hostname('test1.example.com') in host)
        assert_false(Hostname('test1.example.com', '2.3.4.5') in host)

    def test_str(self):
        host = Host('test1')
        assert_equals(host.__str__(), 'Host test1')

    def test_repr(self):
        host = Host('test1')
        assert_equals(host.__repr__(), '<Host test1>')


class TestHostnameList(object):
    def test_indexing(self):
        hosts = HostnameList()
        hosts.add('test1')
        assert_equals(hosts[0].name, 'test1')
        hosts.add('test2')
        assert_equals(hosts[1].name, 'test2')
        assert_equals(hosts[-1].name, 'test2')

    def test_deletion(self):
        hosts = HostnameList()
        hosts.add('test1')
        assert_equals(len(hosts), 1)
        hosts.add('test2')
        assert_equals(len(hosts), 2)
        del hosts[-1]
        assert_equals(len(hosts), 1)

    def test_length(self):
        hosts = HostnameList()
        hosts.add('test1')
        hosts.add('test2')
        assert_equals(len(hosts), 2)
        hosts.add('test1')
        assert_equals(len(hosts), 2)

    def test_itr(self):
        hosts = HostnameList()
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
        hosts = HostnameList()
        hosts.add('test1')
        assert_in('test1', hosts)
        assert_not_in('test2', hosts)

    def test_add_fail(self):
        hosts = HostnameList()
        hosts.add('test1', '1.1.1.1')
        assert_equals(len(hosts), 1)
        assert_raises(TypeError, hosts.add)
        assert_equals(len(hosts), 1)
        hosts.add(ip='1.1.1.1')
        assert_equals(len(hosts), 1)
        hosts.add('1.1.1.1')
        assert_equals(len(hosts), 1)

    def test_get(self):
        hosts = HostnameList()
        hosts.add('test')
        assert_equals(hosts.get('test'), Hostname('test'))
        assert_equals(hosts.get('test'), Hostname('test'))
        assert_equals(hosts.get('test'), Hostname('test'))
        assert_equals(hosts.get('test1'), None)
        hosts.add('test.example.com')
        assert_equals(hosts.get('test'), Hostname('test'))
        assert_equals(hosts.get('test.example.com'), Hostname('test'))
        assert_equals(hosts.get('test'), Hostname('test.example.com'))
        assert_equals(hosts.get('test.example.com'), Hostname('test.example.com'))

    def test_contains_host(self):
        host = HostnameList()
        host.add(Hostname('test', '1.2.3.4'))
        assert_true('test' in host)
        assert_true(Hostname('test') in host)
        assert_true(Hostname('test', '1.2.3.4') in host)
        assert_true(Hostname('test.example.com') in host)
        assert_true(Hostname('test.example.com', '1.2.3.4') in host)

        assert_false('test1' in host)
        assert_false(Hostname('test1') in host)
        assert_false(Hostname('test1', '2.3.4.5') in host)
        assert_false(Hostname('test1.example.com') in host)
        assert_false(Hostname('test1.example.com', '2.3.4.5') in host)

    def test_contains_ip(self):
        host = Host('test1', '1.2.3.4')
        assert_in('1.2.3.4', host)
        assert_not_in('2.3.4.5', host)

    def test_repr(self):
        hosts = HostnameList()
        hosts.add('1.2.3.4')
        assert_equals(hosts.__repr__(), '<HostList \'1.2.3.4\'>')
        hosts.add('2.3.4.5')
        hosts.add('3.4.5.6')
        hosts.add('4.5.6.7')
        assert_equals(hosts.__repr__(), '<HostList \'1.2.3.4, 2.3.4.5, 3.4.5.6\'>')

    def test_str(self):
        hosts = HostnameList()
        hosts.add('1.2.3.4')
        assert_equals(hosts.__str__(), 'HostList (1)')
        hosts.add('2.3.4.5')
        hosts.add('3.4.5.6')
        hosts.add('4.5.6.7')
        assert_equals(hosts.__str__(), 'HostList (4)')
