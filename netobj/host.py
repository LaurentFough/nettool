# -*- coding: utf-8 -*-

import re
from ipv4address import IPv4Address


class HostEntry(object):
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
        HostEntry._validate_base(value)
        if len(value) < 1:
            raise ValueError("'{}' hostname too short. Hostname be between 1-63 characters long".format(value))
        if len(value) > 63:
            raise ValueError("'{}' hostname too long. Hostname be between 1-63 characters long".format(value))

    def _validate_domain(self, value):
        fqdn = HostEntry._build_fqdn(self.name, value)
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
        return HostEntry._clean_base(value).strip('.')

    @staticmethod
    def _clean_domain(value):
        return HostEntry._clean_base(value).strip('.')

    @staticmethod
    def _clean_name(value):
        return HostEntry._clean_base(value)

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
            value = HostEntry._clean_name(value)
            HostEntry._validate_name(value)
        self._name = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is None:
            value = ''
        else:
            value = HostEntry._clean_domain(value)
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
            value = HostEntry._clean_ip(value)
            HostEntry._validate_ip(value)
        self._ip = value

    def __str__(self):
        return HostEntry._build_fqdn(self.name, self.domain)

    def __repr__(self):
        ip = ''
        if self.ip:
            ip = ' {}'.format(self.ip)
        return '<Host {}{}>'.format(HostEntry._build_fqdn(self.name, self.domain), ip)

    def __eq__(self, value):
        if isinstance(value, basestring):
            try:
                ip = IPv4Address(value)
                return ip == self.ip
            except:
                pass
            if '.' in value:
                value = HostEntry._clean_fqdn(value)
                return value == self.fqdn
            else:
                value = HostEntry._clean_name(value)
                return value == self.name
        elif isinstance(value, HostEntry):
            if self.fqdn == value.fqdn and self.ip == value.ip:
                return True
            if self.ip == value.ip:
                return True
            if self.name == value.name:
                return True
        return False

    def __ne__(self, value):
        return not self.__eq__(value)


class HostEntryList(object):
    def __init__(self):
        self._host_entries = list()

    def add(self, value):
        """ Adds a new entry to the host list """
        if value not in self:
            self._append(value)

    def remove(self, value):
        """ Remove an entry from the host list """
        if value in self._host_entries:
            self._host_entries.remove(value)

    def _append(self, value):
        if not isinstance(value, HostEntry):
            value = HostEntry(value)
        self._host_entries.append(value)

    def __contains__(self, value):
        for host_entry in self._host_entries:
            if host_entry == value:
                return True
        return False

    def __len__(self):
        return len(self._host_entries)

    def __iter__(self):
        return self

    def next(self):
        if not hasattr(self, '_itr_current'):
            self._itr_current = 0

        if self._itr_current > len(self._host_entries) - 1:
            self._itr_current = 0
            raise StopIteration
        else:
            self._itr_current += 1
            return self._host_entries[self._itr_current - 1]

    def __str__(self):
        return 'HostList ({})'.format(len(self._host_entries))

    def __repr__(self):
        if len(self._host_entries) > 3:
            sample = ', '.join([str(x) for x in self._host_entries[0:3]])
        else:
            sample = ', '.join([str(x) for x in self._host_entries])
        return '<HostList \'{}\'>'.format(sample)


class Host(HostEntryList):
    """ Represents all the names and IPs referring to the same host """

    def __init__(self, value):
        super(Host, self).__init__()
        self.add(value)

    @property
    def display_name(self):
        if not hasattr(self, '_display_name'):
            if not len(self._host_entries):
                self._display_name = 'unknown'
            else:
                self._display_name = self._host_entries[0].name
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        value = HostEntry._clean_name(value)
        HostEntry._validate_name(value)
        if value not in self._host_entries:
            raise ValueError('Invalid display name \'{}\'. Value not found in the hostname list'.format(value))
        else:
            self._display_name = value

    def __str__(self):
        return 'Host {}'.format(self.display_name)

    def __repr__(self):
        return '<Host {}>'.format(self.display_name)
