# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equals, assert_raises
from nose.tools import assert_true, assert_false

from nettool.layer.network_layer import NetworkLayer


class TestNetworkLayer(object):

    def setup(self):
        self.invalid_types = (1, False, True)
        self.invalid_values = ('network', '1.2.3.4.5')

    def test_initialization(self):
        assert_equals(NetworkLayer(source='1.2.3.4').source, '1.2.3.4/32')
        assert_equals(NetworkLayer(source='1.2.3.4/24').source, '1.2.3.0/24')
        assert_equals(NetworkLayer(destination='1.2.3.4').destination, '1.2.3.4/32')
        assert_equals(NetworkLayer(destination='1.2.3.4/24').destination, '1.2.3.0/24')
        layer = NetworkLayer(source='1.2.3.4/24', destination='5.6.7.8/24')
        assert_equals(layer.source, '1.2.3.0/24')
        assert_equals(layer.destination, '5.6.7.0/24')
        layer = NetworkLayer()
        assert_equals(layer.source, '0.0.0.0/0')
        assert_equals(layer.destination, '0.0.0.0/0')

    def test_initialization_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, NetworkLayer, value, '1.2.3.4')
            assert_raises(ValueError, NetworkLayer, '1.2.3.4', value)

    def test_setter(self):
        layer = NetworkLayer()
        layer.source = '1.2.3.4/24'
        assert_equals(layer.source, '1.2.3.0/24')
        layer.destination = '1.2.3.4/24'
        assert_equals(layer.destination, '1.2.3.0/24')

    def test_setter_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, setattr, NetworkLayer(), 'source', value)
            assert_raises(ValueError, setattr, NetworkLayer(), 'destination', value)

    def test_repr(self):
        layer = NetworkLayer()
        rep = layer.__repr__
        rep_txt = "<NetworkLayer 0.0.0.0/0 0.0.0.0/0>"
        assert_equals(rep(), rep_txt)
        rep_txt = "<NetworkLayer 10.0.0.0/8 0.0.0.0/0>"
        layer.source = '10.0.0.0/8'
        assert_equals(rep(), rep_txt)
        rep_txt = "<NetworkLayer 10.0.0.0/8 192.168.0.0/16>"
        layer.destination = '192.168.2.1/16'
        assert_equals(rep(), rep_txt)

    def test_equality(self):
        layer_a = NetworkLayer(source='1.2.3.4')
        layer_b = NetworkLayer(source='1.2.3.4')
        assert_equals(layer_a, layer_b)

    def test_inequality(self):
        layer_a = NetworkLayer(source='1.2.3.4')
        layer_b = NetworkLayer(source='1.2.3.5')
        assert_not_equals(layer_a, layer_b)

    def test_equality_invalid(self):
        layer = NetworkLayer()
        for value in self.invalid_values:
            assert_raises(TypeError, layer.__eq__, value)

    def test_contains(self):
        layer_narrow = NetworkLayer(source='1.2.3.0/24')
        layer_wide = NetworkLayer()
        assert_true(layer_narrow in layer_wide)
        assert_false(layer_narrow not in layer_wide)

        assert_true(layer_wide not in layer_narrow)

    def test_contains_invalid(self):
        layer = NetworkLayer()
        for value in self.invalid_values:
            assert_raises(TypeError, layer.__contains__, value)

    def test_from_string(self):
        from_string = NetworkLayer.from_string
        layer = from_string('0.0.0.0/0 1.2.3.4/24')

        assert_equals(layer.source, '0.0.0.0/0')
        assert_equals(layer.destination, '1.2.3.0/24')
        layer = from_string('0.0.0.0 1.2.3.4')
        assert_equals(layer.source, '0.0.0.0/32')
        assert_equals(layer.destination, '1.2.3.4/32')

    def test_from_string_invalid(self):
        from_string = NetworkLayer.from_string
        for value in self.invalid_types:
            assert_raises(TypeError, from_string, value)
        for value in self.invalid_values:
            assert_raises(ValueError, from_string, value)

    def test_group_getter(self):
        nl = NetworkLayer()
        new_name = 'new name'
        nl.source.name = new_name
        assert_equals(nl.source.name, new_name)
