# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equals, assert_raises
from nose.tools import assert_true, assert_false

from nettool.ip_layer import IPLayer


class TestIPLayer(object):

    def setup(self):
        self.invalid_values = (1, False, True, 'network')

    def test_initialization(self):
        assert_equals(IPLayer(source='1.2.3.4').source, '1.2.3.4/32')
        assert_equals(IPLayer(source='1.2.3.4/24').source, '1.2.3.0/24')
        assert_equals(IPLayer(destination='1.2.3.4').destination, '1.2.3.4/32')
        assert_equals(IPLayer(destination='1.2.3.4/24').destination, '1.2.3.0/24')
        layer = IPLayer(source='1.2.3.4/24', destination='5.6.7.8/24')
        assert_equals(layer.source, '1.2.3.0/24')
        assert_equals(layer.destination, '5.6.7.0/24')
        layer = IPLayer()
        assert_equals(layer.source, '0.0.0.0/0')
        assert_equals(layer.destination, '0.0.0.0/0')

    def test_initialization_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, IPLayer, value, '1.2.3.4')
            assert_raises(ValueError, IPLayer, '1.2.3.4', value)

    def test_setter(self):
        layer = IPLayer()
        layer.source = '1.2.3.4/24'
        assert_equals(layer.source, '1.2.3.0/24')
        layer.destination = '1.2.3.4/24'
        assert_equals(layer.destination, '1.2.3.0/24')

    def test_setter_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, setattr, IPLayer(), 'source', value)
            assert_raises(ValueError, setattr, IPLayer(), 'destination', value)

    def test_repr(self):
        layer = IPLayer()
        assert_equals(layer.__repr__(), '<IPLayer 0.0.0.0/0 0.0.0.0/0>')
        layer.source = '10.0.0.0/8'
        assert_equals(layer.__repr__(), '<IPLayer 10.0.0.0/8 0.0.0.0/0>')
        layer.destination = '192.168.2.1/16'
        assert_equals(layer.__repr__(), '<IPLayer 10.0.0.0/8 192.168.0.0/16>')

    def test_equality(self):
        layer_a = IPLayer(source='1.2.3.4')
        layer_b = IPLayer(source='1.2.3.4')
        assert_equals(layer_a, layer_b)

    def test_inequality(self):
        layer_a = IPLayer(source='1.2.3.4')
        layer_b = IPLayer(source='1.2.3.5')
        assert_not_equals(layer_a, layer_b)

    def test_equality_invalid(self):
        layer = IPLayer()
        for value in self.invalid_values:
            assert_raises(TypeError, layer.__eq__, value)

    def test_contains(self):
        layer_narrow = IPLayer(source='1.2.3.0/24')
        layer_wide = IPLayer()
        assert_true(layer_narrow in layer_wide)
        assert_false(layer_narrow not in layer_wide)

        assert_true(layer_wide not in layer_narrow)

    def test_contains_invalid(self):
        layer = IPLayer()
        for value in self.invalid_values:
            assert_raises(TypeError, layer.__contains__, value)

    def test_from_string(self):
        from_string = IPLayer.from_string
        layer = from_string('0.0.0.0/0 1.2.3.4/24')
        assert_equals(layer.source, '0.0.0.0/0')
        assert_equals(layer.destination, '1.2.3.0/24')
        layer = from_string('0.0.0.0 1.2.3.4')
        assert_equals(layer.source, '0.0.0.0/32')
        assert_equals(layer.destination, '1.2.3.4/32')

    def test_from_string_invalid(self):
        from_string = IPLayer.from_string
        invalid_strings = (1, False, '0.0.0.0 1')
        for value in invalid_strings:
            assert_raises(ValueError, from_string, value)
