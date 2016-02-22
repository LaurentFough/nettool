# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_not_equals
from nose.tools import assert_is_instance, assert_in, assert_not_in

from nettool.transport_layer import TransportLayer
from nettool.transport_group import TransportGroup
from nettool.transport_address import TransportAddress


class TestTransportLayer(object):

    def setup(self):
        self.invalid_values = ('port', )
        self.invalid_types = (0, True, False)
        self.invalid_contains = ('port', 0, True, False)

    def test_initialization(self):
        group = TransportGroup()
        group.add(TransportAddress(low=1, high=2))
        layer = TransportLayer(source='1-2', destination='2-3')
        assert_equals(layer.source, group)
        group = TransportGroup()
        group.add(TransportAddress(low=2, high=3))
        assert_equals(layer.destination, group)

    def test_initialization_defaults(self):
        layer = TransportLayer()
        assert_equals(layer.source, TransportGroup())
        assert_equals(layer.destination, TransportGroup())
        assert_is_instance(layer.source, TransportGroup)
        assert_is_instance(layer.destination, TransportGroup)

    def test_initialization_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, TransportLayer, value)
        for value in self.invalid_types:
            assert_raises(TypeError, TransportLayer, value)

    def test_src_dst_setter(self):
        layer = TransportLayer()
        for side in ('source', 'destination'):
            setattr(layer, side, '2-5')
            side_attr = getattr(layer, side)
            assert_is_instance(side_attr, TransportGroup)
            assert_in(2, side_attr)
            assert_in(5, side_attr)
            assert_not_in(6, side_attr)
            assert_not_in(1, side_attr)

    def test_setter_invalid(self):
        layer = TransportLayer()
        assert_raises(ValueError, setattr, layer, 'source', 'invalid')
        assert_raises(ValueError, setattr, layer, 'destination', 'invalid')

    def test_repr(self):
        layer = TransportLayer()
        layer.source.name = 'src'
        layer.destination.name = 'dst'
        assert_equals(layer.__repr__(), "<TransportLayer 'src' 'dst'>")

    def test_equality(self):
        layer01 = TransportLayer()
        layer02 = TransportLayer()
        assert_equals(layer01, layer02)
        layer01.source.add('1-2')
        layer02.source.add('1-2')
        assert_equals(layer01, layer02)
        layer01.destination.add('1-2')
        layer02.destination.add('1-2')
        assert_equals(layer01, layer02)

    def test_inequality(self):
        layer01 = TransportLayer()
        layer02 = TransportLayer()
        layer01.source.add('1-2')
        assert_not_equals(layer01, layer02)
        layer02.source.add('1-2')
        layer01.destination.add('1-2')
        assert_not_equals(layer01, layer02)

    def test_contains(self):
        layer01 = TransportLayer()
        layer01.source.add('1-2')
        layer02 = TransportLayer()
        assert_in(layer01, layer02)
        assert_not_in(layer02, layer01)

    def test_contains_invalid(self):
        layer = TransportLayer()
        for value in self.invalid_contains:
            assert_raises(TypeError, layer.__contains__, value)
