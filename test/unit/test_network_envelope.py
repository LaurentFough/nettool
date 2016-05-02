# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from nettool.layer.network_envelope import NetworkEnvelope


class TestNetworkEnvelope(object):

    def setup(self):
        self.invalid_type = (1, False, True, 'network')

    def test_clean_build_string(self):
        clean = NetworkEnvelope._clean_build_string
        assert_equals(clean(' hello  world  '), 'hello world')
