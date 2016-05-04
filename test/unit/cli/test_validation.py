# -*- coding: utf-8 -*-

from mock import Mock

from nettool.cli.validation import ArgumentValidation


class TestArgumentValidation(object):

    @classmethod
    def setup_class(cls):
        cls.context = Mock(name='ClickContext')
        cls.param = Mock(name='ClickParameter')

    @classmethod
    def _get_validator_arguments(cls, value):
        return [cls.context, cls.param, value]

    def test_hostname(self):
        valid_hostname = 'host.example.com'
        arguments = self._get_validator_arguments(valid_hostname)
        assert ArgumentValidation.hostname(*arguments) == valid_hostname
