# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_not_equals, assert_true
from nose.tools import assert_false

from nettool.transport_layer import TransportLayer


class TestTransportLayer(object):

    def setup(self):
        self.invalid_port_values = (0, 65536)
        self.invalid_port_types = (True, False, 'port')

    def test_initialization_defaults(self):
        layer = TransportLayer()
        assert_equals(layer.low, 1)
        assert_equals(layer.high, 65535)

    def test_initialization(self):
        assert_equals(TransportLayer(1).low, 1)
        assert_equals(TransportLayer(1).high, 1)
        assert_equals(TransportLayer(high=1).low, 1)
        assert_equals(TransportLayer(high=1).high, 1)
        assert_equals(TransportLayer(low=1, high=2).low, 1)
        assert_equals(TransportLayer(low=1, high=2).high, 2)
        assert_equals(TransportLayer(low='1', high='2').low, 1)

    def test_initialization_invalid(self):
        for value in self.invalid_port_values:
            assert_raises(ValueError, TransportLayer, value)
        for value in self.invalid_port_types:
            assert_raises(TypeError, TransportLayer, value)

    def test_setter(self):
        layer = TransportLayer()
        layer.low = 1
        assert_equals(layer.low, 1)
        layer.high = 1
        assert_equals(layer.high, 1)

    def test_setter_invalid(self):
        for attr in ('low', 'high'):
            for value in self.invalid_port_values:
                assert_raises(ValueError, setattr, TransportLayer(), attr, value)
            for value in self.invalid_port_types:
                assert_raises(TypeError, setattr, TransportLayer(), attr, value)

    def test_repr(self):
        layer = TransportLayer()
        assert_equals(layer.__repr__(), '<TransportLayer 1-65535>')
        layer.low = 3
        assert_equals(layer.__repr__(), '<TransportLayer 3-65535>')
        layer.high = 3
        assert_equals(layer.__repr__(), '<TransportLayer 3>')
        layer.high = 5
        assert_equals(layer.__repr__(), '<TransportLayer 3-5>')

    def test_equality(self):
        layer_a = TransportLayer()
        layer_b = TransportLayer()
        assert_equals(layer_a, layer_b)

    def test_inequality(self):
        layer_a = TransportLayer()
        layer_b = TransportLayer(high=2)
        assert_not_equals(layer_a, layer_b)
        layer_a.low = 2
        layer_b.high = 65535
        assert_not_equals(layer_a, layer_b)

    def test_contains_single_port(self):
        layer_a = TransportLayer()
        assert_true(2 in layer_a)
        assert_false(2 not in layer_a)
        layer_b = TransportLayer(low=2, high=5)
        assert_false(1 in layer_b)
        assert_true(1 not in layer_b)

    def test_contains_transport_layer(self):
        layer_narrow = TransportLayer(low=2, high=5)
        layer_wide = TransportLayer()
        assert_true(layer_narrow in layer_wide)
        assert_false(layer_narrow not in layer_wide)
        assert_false(layer_wide in layer_narrow)
        assert_true(layer_wide not in layer_narrow)

    def test_contains_invalid(self):
        layer = TransportLayer()
        for value in self.invalid_port_values:
            assert_raises(ValueError, layer.__contains__, value)
        for value in self.invalid_port_types:
            assert_raises(TypeError, layer.__contains__, value)
