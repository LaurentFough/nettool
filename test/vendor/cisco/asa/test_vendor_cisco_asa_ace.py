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

    def test_show_run_group_network(self):
        ace = Ace(network='1.2.3.0/24 4.5.6.0/24')
        ace.network.source.name = 'source'
        ace.network.destination.name = 'destination'
        expected = 'permit ip object-group source object-group destination'
        assert_equals(ace.show_run(), expected)

    def test_show_run_group_transport(self):
        ace = Ace(transport=TransportLayer(name='service'))
        expected = 'permit object-group service 0.0.0.0 0.0.0.0 0.0.0.0 0.0.0.0'
        assert_equals(ace.show_run(), expected)
        ace.transport.destination.add('tcp 22')
        ace.transport.destination.add('udp 161')
        assert_equals(ace.show_run(), expected)

    def test_show_run_group_protocol(self):
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
