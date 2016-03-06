# -*- coding: utf-8 -*-

from nettool._tools import list_repr, raise_type_exception


class AddressGroup(object):
    _address_name = 'Generic'
    _default_name = 'Group'
    _default_address = None

    def __init__(self, name=None):
        self.name = name
        self._addresses = list()

    @property
    def name(self):
        value = self._name
        if value is None:
            value = self._default_name
        return value

    @name.setter
    def name(self, value):
        if value is None:
            value = None
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
        value = self.address_builder(value)
        for address in self.addresses:
            if address == value:
                return True
        return False

    @property
    def address_is_default(self):
        """ Is the group set to the default 'any' address? """
        if len(self.addresses) is 0:
            return True
        elif len(self.addresses) is 1:
            cls = self.addresses[0].__class__
            return self.addresses[0] == cls()
        return False

    def add(self, address):
        address = self.address_builder(address)
        existing = self.has(address)
        if not existing:
            self._addresses.append(address)
        return not existing

    def remove(self, value):
        result = False
        value = self.address_builder(value)
        remove_index = None
        for index, address in enumerate(self._addresses):
            if address == value:
                remove_index = index
        if remove_index is not None:
            del self._addresses[remove_index]
            result = True
        return result

    def __repr__(self):
        # print '__repr__ len', len(self)
        if len(self) is 0:
            entries = str(self._default_address)
        elif len(self) is 1:
            entries = self.addresses[0]
        else:
            entries = list_repr(self.addresses, max_entires=3)
        return '<{} {}>'.format(self.__class__.__name__, entries)

    def __str__(self):
        if self._name:
            return self.name
        elif len(self.addresses) == 1:
            return str(self.addresses[0])
        else:
            return str(self._default_address)

    def __eq__(self, key):
        if isinstance(key, basestring):
            key = self.from_string(key)
        if not isinstance(key, self.__class__):
            raise_type_exception(key, (self.__class__, ), 'test equality of')
        if len(key) == self.__len__():
            for address in self._addresses:
                if not key.has(address):
                    return False
            return True
        return False

    def __len__(self):
        return len(self._addresses)

    def __getitem__(self, index):
        return self.addresses[index]

    def __contains__(self, key):
        valid_types = self._address_type + (self.__class__, )
        if not isinstance(key, valid_types):
            key = self.address_builder(key)
        if not isinstance(key, valid_types):
            raise_type_exception(key, valid_types, 'test membership of')
        if isinstance(key, self.__class__):
            found = False
            for key_address in key.addresses:
                for self_address in self.addresses:
                    if self._is_member(key_address, self_address):
                        found = True
                        break
                if not found:
                    return False
                found = False
            return True
        elif isinstance(key, self._address_type):
            for address in self.addresses:
                if self._is_member(key, address):
                    return True
            return False
        else:
            raise_type_exception(key, valid_types, 'membership')
        return False
