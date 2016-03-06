# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equals
from nose.tools import assert_raises, assert_in, assert_not_in

from nettool.ace import Ace
from nettool.network_layer import NetworkLayer
from nettool.transport_layer import TransportLayer
from nettool.transport_layer_builder import TransportLayerBuilder
from nettool.logging_facility import LoggingFacility


class TestAce(object):

    def setup(self):
        self.ace = Ace()
        self.network_layer = NetworkLayer()
        self.transport_layer = TransportLayer()

    def test_initialization_default(self):
        assert_equals(self.ace.network, NetworkLayer())
        assert_equals(self.ace.transport, None)
        assert_equals(self.ace.logging, LoggingFacility())

    def test_network_getter(self):
        assert_equals(self.ace.network, self.network_layer)

    def test_network_setter(self):
        self.ace.network = None
        assert_equals(self.ace.network, NetworkLayer())
        source = '1.2.3.0/24'
        destination = '5.6.0.0/16'
        nl = NetworkLayer.from_string('{} {}'.format(source, destination))
        self.ace.network = NetworkLayer.from_string('{} {}'.format(source, destination))
        assert_equals(self.ace.network, nl)
        assert_equals(self.ace.network.source, source)
        assert_equals(self.ace.network.destination, destination)

    def test_network_setter_invalid(self):
        invalid_types = (1, True)
        invalid_values = ('1.2.3.0/24', '1', '2 3')
        for value in invalid_types:
            assert_raises(TypeError, setattr, self.ace, 'network', value)
        for value in invalid_values:
            assert_raises(ValueError, setattr, self.ace, 'network', value)

    def test_transport_getter(self):
        assert_equals(self.ace.transport, None)
        self.ace.transport = TransportLayer()
        assert_equals(self.ace.transport, self.transport_layer)

    def test_transport_setter(self):
        self.ace.transport = None
        assert_equals(self.ace.transport, None)
        nl = TransportLayerBuilder.build('tcp 1 2 3 4')
        self.ace.transport = TransportLayerBuilder.build('tcp 1 2 3 4')
        assert_in(nl, self.ace.transport)

    def test_transport_setter_invalid(self):
        invalid_types = (True, )
        invalid_values = ('1.2.3.0/24', )
        for value in invalid_types:
            assert_raises(TypeError, setattr, self.ace, 'transport', value)
        for value in invalid_values:
            assert_raises(ValueError, setattr, self.ace, 'transport', value)

    def test_logging_getter(self):
        self.logging = 2
        assert_equals(self.logging, LoggingFacility(2))

    def test_logging_setter(self):
        for value in (LoggingFacility(2), 2, 'critical'):
            self.ace.logging = value
            assert_equals(self.ace.logging, LoggingFacility(2))
            assert_not_equals(self.ace.logging, LoggingFacility(3))
            assert_not_equals(self.ace.logging, LoggingFacility(1))

    def test_logging_setter_invalid(self):
        invalid_types = (True, )
        invalid_values = ('invalid', )
        for value in invalid_types:
            assert_raises(TypeError, setattr, self.ace, 'logging', value)
        for value in invalid_values:
            assert_raises(ValueError, setattr, self.ace, 'logging', value)

    def test_eqaulity(self):
        aces = list()
        for index in range(2):
            ace = Ace()
            ace.network = NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24')
            ace.transport = TransportLayerBuilder.build('tcp 1024 65535 22 22')
            ace.logging = LoggingFacility.from_string('warning')
            aces.append(ace)
        assert_equals(aces[0], aces[1])

    def test_eqaulity_invalid(self):
        invalid_types = (True, 2, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, self.ace.__eq__, value)

    def test_ineqaulity(self):
        ace = Ace()
        ace.network = NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24')
        ace.transport = TransportLayerBuilder.build('tcp 1024 65535 22 22')
        ace.logging = LoggingFacility.from_string('warning')
        assert_not_equals(Ace(), ace)
        assert_not_equals(Ace(permit=False), Ace())
        assert_not_equals(Ace(logging=1), Ace())
        ace = Ace()
        ace.network = NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24')
        assert_not_equals(ace, Ace())
        ace = Ace()
        ace.transport = TransportLayerBuilder.build('tcp 1024 65535 22 22')
        assert_not_equals(ace, Ace())

    def test_ineqaulity_invalid(self):
        invalid_types = (True, 2, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, self.ace.__ne__, value)

    def test_contains(self):
        ace = Ace()
        assert_in(ace, Ace())
        ace = Ace(network=NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24'))
        assert_in(ace, Ace())
        ace = Ace(transport=TransportLayerBuilder.build('tcp 1024 65535 22 22'))
        assert_in(ace, Ace())
        ace = Ace(logging=2)
        assert_in(ace, Ace(logging=3))

    def test_not_contains(self):
        ace = Ace(network=NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24'))
        assert_not_in(Ace(), ace)
        ace = Ace(transport=TransportLayerBuilder.build('tcp 1024 65535 22 22'))
        assert_not_in(Ace(), ace)
        ace = Ace(logging='warning')
        assert_not_in(Ace(), ace)

    def test_repr(self):
        assert_equals(self.ace.__repr__(), '<ACE {}>'.format(str(self.ace)))

    def test_str_default(self):
        expected = 'permit ip 0.0.0.0/0 0.0.0.0/0'
        ace = Ace()
        assert_equals(ace.__str__(), expected)

    def test_str_deny(self):
        ace = Ace(permit=False, network='1.2.3.4 5.6.7.8')
        expected = 'deny ip 1.2.3.4/32 5.6.7.8/32'
        assert_equals(ace.__str__(), expected)

    def test_str_unnamed_groups_default_transport(self):
        ace = Ace(network='1.2.3.4 5.6.7.8')
        expected = 'permit ip 1.2.3.4/32 5.6.7.8/32'
        assert_equals(ace.__str__(), expected)

    def test_str_unnamed_groups_default_tcp_transport(self):
        ace = Ace(network='1.2.3.4 5.6.7.8', transport='tcp 1-65535 1-65535')
        expected = 'permit tcp 1.2.3.4/32 5.6.7.8/32'
        assert_equals(ace.__str__(), expected)

    def test_str_unnamed_groups_default_udp_transport(self):
        ace = Ace(network='1.2.3.4 5.6.7.8', transport='udp 1-65535 1-65535')
        expected = 'permit udp 1.2.3.4/32 5.6.7.8/32'
        assert_equals(ace.__str__(), expected)

    def test_str_unnamed_groups_full_transport(self):
        ace = Ace(network='1.2.3.4 5.6.7.8')
        ace.transport = 'tcp 1-21 22-22'
        expected = 'permit tcp 1.2.3.4/32 1-21 5.6.7.8/32 22'
        assert_equals(ace.__str__(), expected)

    def tst_str_unnamed_groups_destination_transport(self):
        ace = Ace(network='1.2.3.4 5.6.7.8', transport=22)
        expected = 'permit 1.2.3.4/32 5.6.7.8/32 22'
        assert_equals(ace.__str__(), expected)
        ace.transport = 'tcp 1-65535 22-22'
        expected = 'permit 1.2.3.4/32 5.6.7.8/32 22'
        assert_equals(ace.__str__(), expected)
