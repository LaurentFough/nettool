# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_not_equals, assert_true
from nose.tools import assert_false, assert_in, assert_not_in, assert_is_instance

from nettool.transport_address import TransportAddress


class TestTransportAddress(object):

    def setup(self):
        self.invalid_port_values = (0, 65536)
        self.invalid_port_types = (True, False)

    def test_initialization_defaults(self):
        layer = TransportAddress()
        assert_equals(layer.low, 1)
        assert_equals(layer.high, 65535)

    def test_initialization(self):
        assert_equals(TransportAddress(1).low, 1)
        assert_equals(TransportAddress(1).high, 1)
        assert_equals(TransportAddress(high=1).low, 1)
        assert_equals(TransportAddress(high=1).high, 1)
        assert_equals(TransportAddress(low=1, high=2).low, 1)
        assert_equals(TransportAddress(low=1, high=2).high, 2)
        assert_equals(TransportAddress(low='1', high='2').low, 1)

    def test_initialization_invalid(self):
        for value in self.invalid_port_values:
            assert_raises(ValueError, TransportAddress, value)
        for value in self.invalid_port_types:
            assert_raises(TypeError, TransportAddress, value)

    def test_setter(self):
        layer = TransportAddress()
        layer.low = 1
        assert_equals(layer.low, 1)
        layer.high = 1
        assert_equals(layer.high, 1)

    def test_setter_invalid(self):
        for attr in ('low', 'high'):
            for value in self.invalid_port_values:
                assert_raises(ValueError, setattr, TransportAddress(), attr, value)
            for value in self.invalid_port_types:
                assert_raises(TypeError, setattr, TransportAddress(), attr, value)

    def test_repr(self):
        layer = TransportAddress()
        assert_equals(layer.__repr__(), '<TransportAddress 1-65535>')
        layer.low = 3
        assert_equals(layer.__repr__(), '<TransportAddress 3-65535>')
        layer.high = 3
        assert_equals(layer.__repr__(), '<TransportAddress 3>')
        layer.high = 5
        assert_equals(layer.__repr__(), '<TransportAddress 3-5>')

    def test_str(self):
        layer = TransportAddress()
        assert_equals(layer.__str__(), 'Port 1-65535')
        layer.low = 3
        assert_equals(layer.__str__(), 'Port 3-65535')
        layer.high = 3
        assert_equals(layer.__str__(), 'Port 3')
        layer.high = 5
        assert_equals(layer.__str__(), 'Port 3-5')

    def test_equality(self):
        layer_a = TransportAddress()
        layer_b = TransportAddress()
        assert_equals(layer_a, layer_b)

    def test_inequality(self):
        layer_a = TransportAddress()
        layer_b = TransportAddress(high=2)
        assert_not_equals(layer_a, layer_b)
        layer_a.low = 2
        layer_b.high = 65535
        assert_not_equals(layer_a, layer_b)

    def test_contains_single_port(self):
        layer_a = TransportAddress()
        assert_in(2, layer_a)
        assert_false(2 not in layer_a)
        layer_b = TransportAddress(low=2, high=5)
        assert_not_in(1, layer_b)
        assert_true(1 not in layer_b)

    def test_contains_transport_string(self):
        layer = TransportAddress.from_string('1-2')
        assert_in('1-2', layer)
        assert_not_in('2-3', layer)

    def test_contains_transport_layer(self):
        layer_narrow = TransportAddress(low=2, high=5)
        layer_wide = TransportAddress()
        assert_true(layer_narrow in layer_wide)
        assert_false(layer_narrow not in layer_wide)
        assert_false(layer_wide in layer_narrow)
        assert_true(layer_wide not in layer_narrow)

    def test_contains_invalid(self):
        layer = TransportAddress()
        for value in self.invalid_port_values:
            assert_raises(ValueError, layer.__contains__, value)
        for value in self.invalid_port_types:
            assert_raises(TypeError, layer.__contains__, value)

    def test_from_string(self):
        from_string = TransportAddress.from_string
        address = from_string(1)
        assert_is_instance(address, TransportAddress)
        assert_equals(address.low, 1)
        assert_equals(address.high, 1)
        address = from_string('2')
        assert_equals(address.low, 2)
        assert_equals(address.high, 2)
        string_inits = ('1-2', ' 1 - 2 ', ' 1   2  ', '1  -  2')
        for string_init in string_inits:
            address = from_string(string_init)
            assert_equals(address.low, 1)
            assert_equals(address.high, 2)

    def test_from_string_invalid(self):
        from_string = TransportAddress.from_string
        assert_raises(TypeError, from_string, False)
        invalid_value_strings = ('port', '1-2-3', '1 2 3', 'port 2')
        for value in invalid_value_strings:
            assert_raises(ValueError, from_string, value)
