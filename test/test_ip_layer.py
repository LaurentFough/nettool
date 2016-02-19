# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises

from nettool.ip_layer import IPLayer


class TestIPLayer(object):

    def setup(self):
        pass

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
        assert_raises(ValueError, IPLayer, 1, '1.2.3.4')
        assert_raises(ValueError, IPLayer, '1.2.3.4', 2)

    def test_setter(self):
        layer = IPLayer()
        layer.source = '1.2.3.4/24'
        assert_equals(layer.source, '1.2.3.0/24')
        layer.destination = '1.2.3.4/24'
        assert_equals(layer.destination, '1.2.3.0/24')

    def test_setter_invalid(self):
        assert_raises(ValueError, setattr, IPLayer(), 'source', 1)
        assert_raises(ValueError, setattr, IPLayer(), 'destination', 1)
