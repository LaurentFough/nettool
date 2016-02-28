# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equals
from nose.tools import assert_raises, assert_in, assert_not_in

from nettool.ace import Ace
from nettool.network_layer import NetworkLayer
from nettool.transport_layer import TransportLayer
from nettool.logging_facility import LoggingFacility


class TestAce(object):

    def setup(self):
        self.ace = Ace()
        self.network_layer = NetworkLayer()
        self.transport_layer = TransportLayer()

    def test_initialization_default(self):
        assert_equals(self.ace.network, NetworkLayer())
        assert_equals(self.ace.transport, TransportLayer())
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
        assert_equals(self.ace.transport, self.transport_layer)

    def test_transport_setter(self):
        self.ace.transport = None
        assert_equals(self.ace.transport, TransportLayer())
        nl = TransportLayer.from_string('tcp 1 2 3 4')
        self.ace.transport = TransportLayer.from_string('tcp 1 2 3 4')
        assert_in(nl, self.ace.transport)

    def test_transport_setter_invalid(self):
        invalid_types = (1, True)
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
            ace.transport = TransportLayer.from_string('tcp 1024 65535 22 22')
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
        ace.transport = TransportLayer.from_string('tcp 1024 65535 22 22')
        ace.logging = LoggingFacility.from_string('warning')
        assert_not_equals(Ace(), ace)
        assert_not_equals(Ace(permit=False), Ace())
        assert_not_equals(Ace(logging=1), Ace())
        ace = Ace()
        ace.network = NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24')
        assert_not_equals(ace, Ace())
        ace = Ace()
        ace.transport = TransportLayer.from_string('tcp 1024 65535 22 22')
        assert_not_equals(ace, Ace())

    def test_ineqaulity_invalid(self):
        invalid_types = (True, 2, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, self.ace.__ne__, value)

    def tst_contains(self):
        ace = Ace()
        assert_in(ace, Ace())
        ace = Ace(network=NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24'))
        assert_in(ace, Ace())
        ace = Ace(transport=TransportLayer.from_string('tcp 1024 65535 22 22'))
        assert_in(ace, Ace())
        ace = Ace(logging='warning')
        assert_in(ace, Ace())

    def tst_not_contains(self):
        ace = Ace(network=NetworkLayer.from_string('1.2.3.0/24 2.3.4.0/24'))
        assert_not_in(Ace(), ace)
        ace = Ace(transport=TransportLayer.from_string('tcp 1024 65535 22 22'))
        assert_not_in(Ace(), ace)
        ace = Ace(logging='warning')
        assert_not_in(Ace(), ace)

    def test_repr(self):
        assert_equals(self.ace.__repr__(), '<ACE {}>'.format(str(self.ace)))

    def test_str(self):
        expected = 'permit src_net src_tran dst_net dst_tran'
        ace = Ace()
        ace.network.source.name = 'src_net'
        ace.transport.source.name = 'src_tran'
        ace.network.destination.name = 'dst_net'
        ace.transport.destination.name = 'dst_tran'
        assert_equals(ace.__str__(), expected)
