# -*- coding: utf-8 -*-

# import ipaddress
from ipv4address import IPv4Address

from nettool.nettest import NetTest as nu


class Hostname(object):
    def __init__(self, name=None, ip=None):
        if isinstance(ip, basestring) and not ip.strip():
            ip = None
        if ip is None and nu.validate.ip(name):
            self.ip = name
            name = None
        else:
            self.ip = ip
        self._initialize_name(name)

    def _initialize_name(self, value):
        self.domain = ''
        if nu.validate.ip(value):
            message = 'Invalid hostname \'{}\'. Hostname cannot be an IP address'.format(value)
            raise ValueError(message)
        if isinstance(value, basestring):
            if '.' in value.strip('.'):
                parts = value.split('.')
                name = parts.pop(0)
                nu.validate.host(name)
                self.name = name
                self.domain = '.'.join(parts)
            else:
                self.name = value
        elif value is None:
            self.name = None
        else:
            message = "Invalid type used in Name initilization: '{}'.".format(type(value).__name__)
            raise TypeError(message)

    # def _initialize_ip(self, value):
    #     self.ip = value

    @staticmethod
    def _build_fqdn(hostname, domain):
        fqdn = ''
        if hostname is None:
            return None
        if len(domain) > 0:
            fqdn = '.'.join([hostname, domain])
        else:
            fqdn = hostname
        return fqdn

    @staticmethod
    def _clean_base(value):
        return value.lower()

    @staticmethod
    def _clean_fqdn(value):
        return Hostname._clean_base(value).strip('.')

    @staticmethod
    def _clean_domain(value):
        return Hostname._clean_base(value).strip('.')

    @staticmethod
    def _clean_name(value):
        return Hostname._clean_base(value)

    @property
    def fqdn(self):
        return self._build_fqdn(self.name, self.domain)

    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = None
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = None
        else:
            value = Hostname._clean_name(value)
            nu.validate.host(value)
        self._name = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is not None and self.name is not None:
            value = Hostname._clean_domain(value)
            nu.validate.hostname(self._build_fqdn(self.name, value), raise_exception=True)
        self._domain = value

    @property
    def ip(self):
        address = self._ip
        if isinstance(address, IPv4Address):
            address = address.exploded
        return address

    @ip.setter
    def ip(self, value):
        if value is None:
            value = None
        else:
            nu.validate.ip(value, raise_exception=True)
            if not isinstance(value, IPv4Address):
                value = IPv4Address(value)
        self._ip = value

    def __str__(self):
        hostname = Hostname._build_fqdn(self.name, self.domain)
        ip = self.ip or ''
        hostname = hostname or ip
        if hostname == ip:
            ip = ''
        hostname = '{} {}'.format(hostname, ip).strip()
        return hostname

    def __repr__(self):
        hostname = Hostname._build_fqdn(self.name, self.domain)
        if hostname is None:
            hostname = 'Unknown'
        ip = ''
        if self.ip:
            ip = ' {}'.format(self.ip)
        return '<Host {}{}>'.format(hostname, ip)

    def __eq__(self, value):
        if isinstance(value, basestring):
            try:
                ip = IPv4Address(value)
                return ip == self.ip
            except ValueError:
                pass
            if '.' in value.rstrip('.'):
                value = Hostname._clean_fqdn(value)
                return value == self.fqdn
            else:
                value = Hostname._clean_name(value)
                return value == self.name
        elif isinstance(value, Hostname):
            if self.domain and value.domain:
                if self.fqdn == value.fqdn:
                    return True
            else:
                if self.name == value.name:
                    return True
            if self.ip and self.ip == value.ip:
                return True
        return False

    def __ne__(self, value):
        return not self.__eq__(value)
