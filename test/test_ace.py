# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises

from nettool.ace import Ace


class TestAce(object):

    def setup(self):
        pass

    def test_initialization_ip(self):
        assert_equals(Ace().source, '0.0.0.0/0')
        assert_equals(Ace(source='1.2.3.4/24').source, '1.2.3.0/24')
        assert_equals(Ace().destination, '0.0.0.0/0')
        assert_equals(Ace(destination='1.2.3.4/24').destination, '1.2.3.0/24')

    def test_ip_layer(self):
        ace = Ace()
        ace.source = '1.2.3.4/24'
        assert_equals(ace.source, '1.2.3.0/24')
        assert_equals(ace.destination, '0.0.0.0/0')
        ace = Ace()
        ace.destination = '1.2.3.4/24'
        assert_equals(ace.source, '0.0.0.0/0')
        assert_equals(ace.destination, '1.2.3.0/24')
