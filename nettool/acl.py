# -*- coding: utf-8 -*-

from nettool.ace import Ace
from nettool._tools import raise_type_exception


class Acl(object):
    _default_name = 'ACL'

    def __init__(self, name=None, default_permit=False, line_increment=1):
        self.name = name
        self._aces = list()
        self.default_permit = default_permit
        self.line_increment = line_increment
        self._current_line = 0
        self.dynamic_line_increment = True

    @property
    def line_increment(self):
        return self._line_increment

    @line_increment.setter
    def line_increment(self, value):
        if isinstance(value, basestring) and value.strip().isdigit():
            value = int(value.strip())
        if not isinstance(value, int):
            raise_type_exception(value, (int, ), 'set')
        self._line_increment = value

    @property
    def default_permit(self):
        return self._default_permit

    @default_permit.setter
    def default_permit(self, value):
        if not isinstance(value, bool):
            raise_type_exception(value, (bool, ), 'set')
        self._default_permit = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = self._default_name
        elif not isinstance(value, basestring):
            raise_type_exception(value, (str, ), 'set')
        self._name = value

    def add(self, ace, line_number=None):
        if not isinstance(ace, Ace):
            raise_type_exception(ace, (Ace, ), 'add')
        if not isinstance(line_number, (int, type(None))):
            raise_type_exception(line_number, (int, ), 'add line number')
        for existing in self._aces:
            if ace == existing:
                return
        self._current_line += 1
        if line_number is None:
            line_number = self._current_line

        if (line_number - 1) > len(self._aces):
            message = 'Line number {} higher than ACEs length {}'
            message = message.format(line_number, len(self._aces))
            raise ValueError(message)
        ace._line_number = line_number
        self._aces.insert(line_number, ace)

    def remove(self, ace):
        if not isinstance(ace, Ace):
            raise_type_exception(ace, (Ace, ), 'remove')
        self._aces.remove(ace)
        self._current_line -= 1

    def permits(self, key):
        return self._test_permission(key, permit=True)

    def allows(self, key):
        return self.permits(key)

    def denies(self, key):
        return self._test_permission(key, permit=False)

    def _test_permission(self, key, permit):
        if not isinstance(key, Ace):
            raise_type_exception(key, (Ace, ), 'test permission of')
        if isinstance(key, Ace):
            key_aces = (key, )
        else:
            key_aces = key._aces

        for key_ace in key_aces:
            for self_ace in self._aces:
                if key_ace in self_ace and self_ace.permit is permit:
                    break
            else:
                return self.default_permit and permit
        return permit

    def __getitem__(self, index):
        return self._aces[index]

    def __len__(self):
        return len(self._aces)

    def __eq__(self, key):
        if not isinstance(key, Acl):
            raise_type_exception(key, (Acl, ), 'test equality of')
        if len(key) == len(self) and key.default_permit == self.default_permit:
            for key_ace in key._aces:
                for self_ace in self._aces:
                    if self_ace == key_ace:
                        break
                else:
                    return False
            return True
        return False

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if not isinstance(key, (Acl, Ace)):
            raise_type_exception(key, (Acl, Ace), 'test membership of')
        if isinstance(key, Ace):
            key_aces = (key, )
        else:
            key_aces = key._aces

        for key_ace in key_aces:
            for self_ace in self._aces:
                if key_ace in self_ace:
                    break
            else:
                return False
        return True

    def __repr__(self):
        cls_name = self.__class__.__name__
        return '<{} {} #{}>'.format(cls_name, self.name, len(self))

    def __str__(self):
        cls_name = self.__class__.__name__
        output = '{} {} #{}'.format(cls_name, self.name, len(self))
        aces = '\n\t'.join([ace.__str__() for ace in self._aces]).strip()
        if aces:
            output = '{}\n\t{}'.format(output, aces)
        return output
