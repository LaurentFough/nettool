# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_not_equals
from nose.tools import assert_is_instance, assert_in, assert_not_in

from nettool.transport_layer import TransportLayer
from nettool.transport_group import TransportGroup


class TestTransportLayer(object):

    def setup(self):
        self.invalid_port_values = (0, 65536)
        self.invalid_port_types = (True, False, 'port')

    def test_initialization(self):
        pass

    def test_initialization_defaults(self):
        layer = TransportLayer()
        assert_is_instance(layer.source, TransportGroup)
        assert_is_instance(layer.destination, TransportGroup)

    def test_initialization_invalid(self):
        for value in self.invalid_port_values:
            pass
            # assert_raises(ValueError, TransportLayer, value)
        for value in self.invalid_port_types:
            pass
            # assert_raises(TypeError, TransportLayer, value)

    def test_setter(self):
        layer = TransportLayer()
        for side in ('source', 'destination'):
            setattr(layer, side, '2-5')
            side_attr = getattr(layer, side)
            print side_attr
            assert_is_instance(side_attr, TransportGroup)
            assert_in(2, side_attr)
            assert_in(5, side_attr)
            print side
            assert_not_in(6, side_attr)
            assert_not_in(1, side_attr)

    def test_setter_invalid(self):
        layer = TransportLayer()
        assert_raises(ValueError, setattr, layer, 'source', 'invalid')

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
        # assert_in(layer01, layer02)
        s = layer02.destination
        print s in layer01.destination
        assert_not_in(layer02, layer01)
