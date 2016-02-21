# -*- coding: utf-8 -*-

from nettool.transport_address import TransportAddress
from nettool._tools import list_repr, raise_type_exception


class TransportGroup(object):
    _default_name = 'Transport Group'

    def __init__(self, name=None):
        self.name = name
        self._addresses = list()

    @property
    def addresses(self):
        if not self._addresses:
            return [TransportAddress()]
        return self._addresses

    @staticmethod
    def _build_transport_address(transport_address):
        if isinstance(transport_address, (basestring, int)):
            transport_address = TransportAddress.from_string(transport_address)
        elif not isinstance(transport_address, TransportAddress):
            raise_type_exception(transport_address, (TransportAddress, ), 'add')
        return transport_address

    def has(self, transport_address):
        """ Returns True if the address is in the group """
        transport_address = TransportGroup._build_transport_address(transport_address)
        for ta in self.addresses:
            if ta == transport_address:
                return True
        return False

    def add(self, transport_address):
        transport_address = TransportGroup._build_transport_address(transport_address)
        existing = self.has(transport_address)
        if not existing:
            self._addresses.append(transport_address)
        return not existing

    def remove(self, transport_address):
        transport_address = TransportGroup._build_transport_address(transport_address)
        remove_index = None
        for index, ta in enumerate(self._addresses):
            if ta == transport_address:
                remove_index = index
        if remove_index is not None:
            del self._addresses[remove_index]
            return True
        return False

    @staticmethod
    def from_string(value):
        transport_address = TransportAddress.from_string(value)
        transport_group = TransportGroup()
        transport_group.add(transport_address)
        return transport_group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = TransportGroup._default_name
        elif not isinstance(value, basestring):
            raise_type_exception(value, (str, ), 'set')
        self._name = value

    def __repr__(self):
        entries = list_repr(self.addresses, max_entires=3)
        return '<{} {}>'.format(self.__class__.__name__, entries)

    def __eq__(self, key):
        if not isinstance(key, TransportGroup):
            self._raise_type_exception(self, key, (TransportGroup, ), 'test equality of')
        if len(key) == self.__len__():
            for address in self._addresses:
                if not key.has(address):
                    return False
            return True
        return False

    def __len__(self):
        return len(self._addresses)

    def __contains__(self, key):
        if not isinstance(key, (TransportGroup, TransportAddress)):
            key = TransportAddress.from_string(key)
        if not isinstance(key, (TransportGroup, TransportAddress)):
            raise_type_exception(key, (TransportGroup, TransportAddress), 'test membership of')
        if isinstance(key, TransportGroup):
            found = False
            for key_address in key.addresses:
                for self_address in self.addresses:
                    if key_address in self_address:
                        found = True
                        break
                if not found:
                    return False
                found = False
            return True
        elif isinstance(key, TransportAddress):
            for address in self.addresses:
                if key in address:
                    return True
            return False
        else:
            raise_type_exception(key, (TransportGroup, TransportAddress), 'membership')
        return False
