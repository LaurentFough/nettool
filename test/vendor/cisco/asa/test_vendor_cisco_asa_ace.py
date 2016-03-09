# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from nose.tools import assert_true, assert_false
from nettool.layer.transport_layer import TransportLayer
from nettool.vendor.cisco.asa.ace import Ace


class TestVendorCiscoAsaAce(object):

    def test_is_grouped(self):
        ace = Ace(network='1.2.3.0/24 4.5.6.0/24', transport='tcp 22')
        assert_false(ace._is_grouped())
        ace.network.source.name = 'source'
        assert_true(ace._is_grouped())
        ace.network.source.name = None
        assert_false(ace._is_grouped())
        ace.transport.name = 'test'
        assert_true(ace._is_grouped())
        ace.transport.name = None
        assert_false(ace._is_grouped())
        ace.transport.source.name = 'test'
        assert_true(ace._is_grouped())
        ace.transport.source.name = None
        assert_false(ace._is_grouped())
        ace.transport.destination.name = 'test'
        assert_true(ace._is_grouped())
        ace.transport.destination.name = None
        assert_false(ace._is_grouped())

    def test_show_run_default(self):
        ace = Ace()
        expected = 'permit ip 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0'
        assert_equals(ace.show_run(), expected)

    def test_show_run_protocol(self):
        ace = Ace(transport='tcp 22')
        ace.transport.destination.name = 'ssh'
        expected = 'permit tcp 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0 object-group ssh'
        assert_equals(ace.show_run(), expected)
        ace.transport.destination.name = None
        ace.transport.source.remove('tcp 1-65535')
        ace.transport.destination.remove('tcp 22')
        ace.transport.source.name = 'snmp-trap'
        ace.transport.source.add('udp 162')
        ace.transport.destination.add('udp 1-65535')
        expected = 'permit udp 0.0.0.0 0.0.0.0 object-group snmp-trap 0.0.0.0 0.0.0.0'
        assert_equals(ace.show_run(), expected)

    def test_show_run_network(self):
        ace = Ace(network='1.2.3.0/24 4.5.6.0/24')
        ace.network.source.name = 'source'
        ace.network.destination.name = 'destination'
        expected = 'permit ip object-group source object-group destination'
        assert_equals(ace.show_run(), expected)

    def test_show_run_transport(self):
        ace = Ace(transport=TransportLayer(name='service'))
        expected = 'permit object-group service 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0'
        assert_equals(ace.show_run(), expected)
        ace.transport.destination.add('tcp 22')
        ace.transport.destination.add('udp 161')
        assert_equals(ace.show_run(), expected)

    def test_show_default(self):
        ace = Ace()
        expected = 'permit ip 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0'
        assert_equals(ace.show(), expected)

    def test_show_protocol(self):
        ace = Ace(transport='tcp 22')
        ace.transport.destination.name = 'ssh'
        expected = 'permit tcp 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0 eq 22'
        assert_equals(ace.show(), expected)
        ace.transport.destination.name = None
        ace.transport.source.remove('tcp 1-65535')
        ace.transport.destination.remove('tcp 22')
        ace.transport.source.name = 'snmp-trap'
        ace.transport.source.add('udp 162')
        ace.transport.destination.add('udp 1-65535')
        expected = 'permit udp 0.0.0.0 0.0.0.0 eq 162 0.0.0.0 0.0.0.0'
        assert_equals(ace.show(), expected)

    def test_show_network(self):
        ace = Ace(network='1.2.3.0/24 4.5.6.0/24')
        ace.network.source.name = 'source'
        ace.network.destination.name = 'destination'
        expected = 'permit ip 1.2.3.0 255.255.255.0 4.5.6.0 255.255.255.0'
        assert_equals(ace.show(), expected)

    def test_show_transport(self):
        ace = Ace(transport=TransportLayer(name='service'))
        expected = 'permit ip 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0'
        assert_equals(ace.show(), expected)
        ace.transport.source.add('tcp 1-65535')
        ace.transport.destination.add('tcp 22')
        expected = 'permit tcp 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0 eq 22'
        assert_equals(ace.show(), expected)
        ace.transport.source.remove('tcp 1-65535')
        ace.transport.source.add('tcp 1-22')
        expected = 'permit tcp 0.0.0.0 0.0.0.0 range 1 22 0.0.0.0 0.0.0.0 eq 22'
        assert_equals(ace.show(), expected)
