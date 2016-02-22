# -*- coding: utf-8 -*-

from nettool._tools import list_repr, raise_type_exception


class AddressGroup(object):
    _default_name = 'Group'
    _default_address = None

    def __init__(self, name=None):
        self.name = name
        self._addresses = list()

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

    @property
    def addresses(self):
        if not self._addresses:
            return [self._default_address]
        return self._addresses

    @staticmethod
    def from_string(cls, value):
        if isinstance(value, basestring):
            value = cls._clean_address(value)
            group = cls()
            group.add(value)
            return group
        raise_type_exception(value, (str, unicode), 'build from')

    def has(self, value):
        """ Returns True if the address is in the group """
        value = self._build_address(value)
        for address in self.addresses:
            if address == value:
                return True
        return False

    def add(self, address):
        address = self._build_address(address)
        existing = self.has(address)
        if not existing:
            self._addresses.append(address)
        return not existing

    def remove(self, value):
        value = self._build_address(value)
        remove_index = None
        for index, address in enumerate(self._addresses):
            if address == value:
                remove_index = index
        if remove_index is not None:
            del self._addresses[remove_index]
            return True
        return False

    def __repr__(self):
        entries = list_repr(self.addresses, max_entires=3)
        return '<{} {}>'.format(self.__class__.__name__, entries)

    def __eq__(self, key):
        if not isinstance(key, self.__class__):
            self._raise_type_exception(self, key, (self.__class__, ), 'test equality of')
        if len(key) == self.__len__():
            for address in self._addresses:
                if not key.has(address):
                    return False
            return True
        return False

    def __len__(self):
        return len(self._addresses)

