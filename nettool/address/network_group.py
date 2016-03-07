# -*- coding: utf-8 -*-

from ipaddress import IPv4Interface, IPv4Network, AddressValueError
from nettool.utilities import raise_type_exception
from nettool.address.address_group import AddressGroup
from nettool.nettest import NetTest as nu


class NetworkGroup(AddressGroup):
    _default_address = IPv4Network(u'0.0.0.0/0')
    _address_type = (IPv4Network, )

    @classmethod
    def _clean_address(cls, network):
        if network is None:
            network = cls._default_address
        else:
            nu.validate.network(network, raise_exception=True)
            network = IPv4Interface(unicode(network)).network
        return network

    @property
    def address_is_default(self):
        """ Is the group set to the default 'any' address? """
        if len(self.addresses) is 0:
            return True
        elif len(self.addresses) is 1:
            return self.addresses[0] == self._default_address
        return False

    @staticmethod
    def address_builder(value):
        if isinstance(value, (basestring)):
            try:
                value = IPv4Interface(unicode(value)).network
            except AddressValueError:
                message = 'Unsupported string initialization format \'{}\''
                message = message.format(value)
                raise ValueError(message)
        elif not isinstance(value, IPv4Network):
            raise_type_exception(value, (IPv4Network, ), 'build with')
        return value

    @staticmethod
    def _is_member(key, member):
        return key.subnet_of(member)

    @classmethod
    def from_string(cls, value):
        address = cls.address_builder(value)
        group = cls()
        group.add(address)
        return group
