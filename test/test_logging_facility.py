# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_in, assert_not_in
from nose.tools import assert_not_equals

from nettool.logging_facility import LoggingFacility


class TestLoggingFacility(object):

    def setup(self):
        self.log = LoggingFacility()
        self.invalid_values = (-1, 'super emergency')
        self.invalid_types = (True, list(), tuple())

    def test_initialization_default(self):
        assert_equals(self.log.level, None)
        assert_equals(self.log.name, 'none')

    def test_initialization(self):
        for index, name in enumerate(LoggingFacility._level_names):
            assert_equals(LoggingFacility(name).level, index)
        for index, name in enumerate(LoggingFacility._level_names):
            assert_equals(LoggingFacility(index).level, index)

    def test_level_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, setattr, self.log, 'level', value)
        for value in self.invalid_types:
            assert_raises(TypeError, setattr, self.log, 'level', value)

    def test_number_getter(self):
        for index, name in enumerate(LoggingFacility._level_names):
            assert_equals(LoggingFacility(name).number, index)

    def test_name_getter(self):
        for index, name in enumerate(LoggingFacility._level_names):
            assert_equals(LoggingFacility(index).name, name)

    def test_contains(self):
        log01 = LoggingFacility(2)
        log02 = LoggingFacility(7)
        assert_in(log01, log02)
        log01 = LoggingFacility(7)
        assert_in(log01, log02)
        assert_in(LoggingFacility(), LoggingFacility())

    def test_not_contains(self):
        log01 = LoggingFacility(2)
        log02 = LoggingFacility(7)
        assert_not_in(log02, log01)
        assert_not_in(LoggingFacility(), log01)

    def test_contains_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, self.log.__contains__, value)
        for value in self.invalid_types:
            assert_raises(TypeError, self.log.__contains__, value)

    def test_equality(self):
        assert_equals(LoggingFacility(2), LoggingFacility(2))
        assert_equals('critical', LoggingFacility(2))

    def test_equality_invalid(self):
        for value in self.invalid_values:
            assert_raises(ValueError, self.log.__eq__, value)
        for value in self.invalid_types:
            assert_raises(TypeError, self.log.__eq__, value)

    def test_inequality(self):
        assert_not_equals(LoggingFacility(2), LoggingFacility(3))
        assert_not_equals(2, LoggingFacility(3))
        assert_not_equals('error', LoggingFacility(3))

    def test_from_string(self):
        from_string = LoggingFacility.from_string
        for index, name in enumerate(LoggingFacility._level_names):
            assert_equals(from_string(index).level, index)
            assert_equals(from_string(str(index)).level, index)
            assert_equals(from_string(name).level, index)
        assert_equals(LoggingFacility.from_string('WARNING  ').level, 4)

    def test_from_string_invalid(self):
        from_string = LoggingFacility.from_string
        for value in self.invalid_values:
            assert_raises(ValueError, from_string, value)
        for value in self.invalid_types:
            assert_raises(TypeError, from_string, value)

    def test_repr(self):
        assert_equals(self.log.__repr__(), '<LoggingFacility none>')
        self.log.level = 'warning'
        assert_equals(self.log.__repr__(), '<LoggingFacility warning>')
