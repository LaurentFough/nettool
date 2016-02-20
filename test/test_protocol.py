# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises

from nettool.protocol_layer import ProtocolLayer


class TestProtocolLayer(object):

    def test_initialization(self):
        assert_equals(ProtocolLayer(name='ip').name, 'ip')

    def test_initialization_invalid(self):
        assert_raises(ValueError, ProtocolLayer, True)

    def test_setter(self):
        layer = ProtocolLayer()
        layer.name = 'tcp'
        assert_equals(layer.name, 'tcp')

    def test_setter_invalid(self):
        assert_raises(ValueError, setattr, ProtocolLayer(), 'name', False)
