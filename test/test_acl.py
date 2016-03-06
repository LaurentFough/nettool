# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_not_equals, assert_true, assert_false
# from nose.tools import assert_equals # , assert_not_equals
from nose.tools import assert_raises, assert_in, assert_not_in

from nettool.acl import Acl
from nettool.ace import Ace
# from nettool.network_layer import NetworkLayer
# from nettool.transport_layer import TransportLayer
# from nettool.logging_facility import LoggingFacility


class TestAcl(object):

    def setup(self):
        pass

    def test_initialization(self):
        assert_equals(Acl('test').name, 'test')

    def test_initialization_default(self):
        assert_equals(Acl().name, Acl._default_name)

    def test_add(self):
        acl = Acl()
        acl.add(Ace())
        assert_equals(len(acl), 1)
        assert_equals(acl[-1]._line_number, 1)
        acl.add(Ace())
        assert_equals(len(acl), 1)
        assert_equals(acl[-1]._line_number, 1)
        acl.add(Ace(logging=2))
        assert_equals(acl[-1]._line_number, 2)

    def test_add_invalid(self):
        acl = Acl()
        invalid_types = (False, 2, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, acl.add, value)
        assert_raises(ValueError, acl.add, Ace(), 2)

    def test_remove(self):
        acl = Acl()
        acl.add(Ace())
        acl.remove(Ace())
        assert_equals(len(acl), 0)

    def test_remove_invalid(self):
        acl = Acl()
        acl.add(Ace())
        assert_raises(ValueError, acl.remove, Ace(permit=False))
        invalid_types = (False, 2, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, acl.remove, value)

    def test_getitem(self):
        acl = Acl()
        ace = Ace()
        acl.add(ace)
        assert_equals(id(acl[0]), id(ace))

    def test_length(self):
        acl = Acl()
        acl.add(Ace())
        assert_equals(len(acl), 1)
        acl.add(Ace(logging=1))
        assert_equals(len(acl), 2)

    def test_eqaulity(self):
        assert_equals(Acl(), Acl())
        acl01 = Acl()
        acl01.add(Ace(logging=2))
        acl02 = Acl()
        acl02.add(Ace(logging=2))
        assert_equals(acl01, acl02)

    def test_eqaulity_invalid(self):
        acl = Acl()
        invalid_types = (False, 1, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, acl.__eq__, value)

    def test_ineqaulity(self):
        acl01 = Acl()
        acl01.add(Ace(logging=2))
        acl02 = Acl()
        assert_not_equals(acl01, acl02)
        acl02.add(Ace())
        assert_not_equals(acl01, acl02)

    def test_ineqaulity_invalid(self):
        acl = Acl()
        invalid_types = (False, 1, 'invalid')
        for value in invalid_types:
            assert_raises(TypeError, acl.__ne__, value)

    def test_contains(self):
        acl = Acl()
        ace = Ace()
        acl.add(ace)
        assert_in(ace, acl)

    def test_not_contains(self):
        acl = Acl()
        ace = Ace()
        assert_not_in(ace, acl)

    def test_repr(self):
        expected = '<Acl test01 #0>'
        assert_equals(Acl('test01').__repr__(), expected)

    def test_str(self):
        acl = Acl('test01')
        expected = 'Acl test01 #0'
        assert_equals(acl.__str__(), expected)
        acl.add(Ace(permit=False, network='1.2.3.0/24 4.5.6.0/24'))
        expected = 'Acl test01 #1\n\tdeny ip 1.2.3.0/24 4.5.6.0/24'
        assert_equals(acl.__str__(), expected)

    def test_permits_ace(self):
        acl = Acl()
        assert_false(acl.permits(Ace()))
        acl.add(Ace())
        assert_true(acl.permits(Ace()))
        acl.remove(Ace())
        acl.add(Ace(network='1.2.3.0/24 4.5.6.0/24'))
        assert_true(acl.permits(Ace(network='1.2.3.4 4.5.6.7')))

    def test_permits_ace_default_permit(self):
        acl = Acl(default_permit=True)
        assert_true(acl.permits(Ace()))
        acl.add(Ace(network='1.2.3.0/24 4.5.6.0/24'))
        assert_true(acl.permits(Ace(network='4.5.6.7 1.2.3.4')))
        acl.remove(Ace(network='1.2.3.0/24 4.5.6.0/24'))
        acl.add(Ace(permit=False, network='1.2.3.0/24 4.5.6.0/24'))
        # print
        # print acl
        # assert_true(False)
        # assert_true(acl.permits(Ace(network='1.2.3.4 4.5.6.7')))

    def test_permits_acl(self):
        pass
        # acl01 = Acl()
        # acl02 = Acl()
        # assert_false(acl01.permits(acl02))

    def test_default_permits(self):
        pass

    def tst_denies(self):
        # TODO: Fix me
        acl = Acl()
        assert_true(acl.denies(Ace()))
