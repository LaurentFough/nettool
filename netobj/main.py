# -*- coding: utf-8 -*-

import re
from ipv4address import IPv4Address


class Host(object):
    def __init__(self, name, ip=None):
        self._initialize_name(name)
        self._initialize_ip(ip)

    def _initialize_name(self, value):
        if isinstance(value, basestring):
            if '.' in value.strip('.'):
                parts = value.split('.')
                self.name = parts.pop(0)
                self.domain = '.'.join(parts)
            else:
                self.name = value
                self.domain = ''
        else:
            raise TypeError("Invalid type used in Name initilization: '{}'.".format(type(value).__name__))

    def _initialize_ip(self, value):
        self.ip = value

    @staticmethod
    def _clean_ip(value):
        return IPv4Address(value)

    @staticmethod
    def _validate_ip(value):
        if not isinstance(value, IPv4Address):
            IPv4Address(value)

    @staticmethod
    def _validate_base(value):
        try:
            if isinstance(value, unicode):
                str(value)
            else:
                unicode(value, encoding='ascii')
        except UnicodeDecodeError as e:
            value = unicode(value, 'utf-8')
            position = re.search(r'in position (\d+):', str(e)).group(1)
            invalid_character = value[int(position)]
            error_message = unicode(u"'{}' invalid character '{}'. Must use ASCII characters".format(value, invalid_character))
            raise ValueError(error_message)
        invalid_character_match = re.search(r'([^0-9a-z\-])', value.lower())
        if invalid_character_match:
            raise ValueError("'{}' invalid character \'{}\'.".format(value, invalid_character_match.group(1)))

    @staticmethod
    def _validate_name(value):
        Host._validate_base(value)
        if len(value) < 1:
            raise ValueError("'{}' hostname too short. Hostname be between 1-63 characters long".format(value))
        if len(value) > 63:
            raise ValueError("'{}' hostname too long. Hostname be between 1-63 characters long".format(value))

    def _validate_domain(self, value):
        fqdn = Host._build_fqdn(self.name, value)
        if len(fqdn) > 253:
            raise ValueError("'{}' is too long. FQDN must be less than 254 characters".format(value))

    @staticmethod
    def _build_fqdn(hostname, domain):
        fqdn = ''
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
        return Host._clean_base(value).strip('.')

    @staticmethod
    def _clean_domain(value):
        return Host._clean_base(value).strip('.')

    @staticmethod
    def _clean_name(value):
        return Host._clean_base(value)

    @property
    def fqdn(self):
        return self._build_fqdn(self.name, self.domain)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = 'unknown'
        else:
            value = Host._clean_name(value)
            Host._validate_name(value)
        self._name = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is None:
            value = ''
        else:
            value = Host._clean_domain(value)
            self._validate_domain(value)
        self._domain = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        if value is None:
            value = None
        else:
            value = Host._clean_ip(value)
            Host._validate_ip(value)
        self._ip = value

    def __str__(self):
        return Host._build_fqdn(self.name, self.domain)

    def __repr__(self):
        ip = ''
        if self.ip:
            ip = ' {}'.format(self.ip)
        return '<Host {}{}>'.format(Host._build_fqdn(self.name, self.domain), ip)

    def __eq__(self, value):
        if isinstance(value, basestring):
            try:
                ip = IPv4Address(value)
                return ip == self.ip
            except:
                pass
            if '.' in value:
                value = Host._clean_fqdn(value)
                return value == self.fqdn
            else:
                value = Host._clean_name(value)
                return value == self.name
        elif isinstance(value, Host):
            if self.fqdn == value.fqdn and self.ip == value.ip:
                return True
            if self.ip == value.ip:
                return True
            if self.name == value.name:
                return True
        return False

    def __ne__(self, value):
        return not self.__eq__(value)
