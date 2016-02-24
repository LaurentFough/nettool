# -*- coding: utf-8 -*-

from ipv4address import IPv4Address

from nettool.nutility import NUtility as nu
from validate import Validate


class Hostname(object):
    def __init__(self, name=None, ip=None):
        try:
            nu.validate.ip(name, raise_exception=True)
        except ValueError:
            pass
        else:
            if ip is not None:
                raise ValueError('Two conflicting IPs specified: {} & {}'.format(name, ip))
            ip = name
            name = None
        self._initialize_name(name)
        self.ip = ip

    def _initialize_name(self, value):
        self.domain = ''
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
            raise TypeError("Invalid type used in Name initilization: '{}'.".format(type(value).__name__))

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
        return self._ip

    @ip.setter
    def ip(self, value):
        if value is None:
            value = None
        else:
            Validate.ip(value)
            if not isinstance(value, IPv4Address):
                value = IPv4Address(value)
        self._ip = value

    def __str__(self):
        hostname = Hostname._build_fqdn(self.name, self.domain)
        if hostname is None:
            hostname = self.ip.exploded
        return '{}'.format(hostname)

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


class HostnameList(object):
    def __init__(self):
        self._host_entries = list()
        self._itr_current = 0

    def add(self, value=None, ip=None):
        """ Adds a new entry to the host list """
        if value is None and ip is None:
            raise TypeError('add requires at least 1 argument. (0 given)')
        self._add(value, ip=ip)

    def _add(self, value=None, ip=None):
        if (value and value not in self) or (ip and ip not in self):
            self._append(value, ip)

    def get(self, value):
        if value in self._host_entries:
            for index, host in enumerate(self._host_entries):
                if host == value:
                    return self[index]
        return None

    def remove(self, value):
        """ Remove an entry from the host list """
        if value in self._host_entries:
            self._host_entries.remove(value)

    def _append(self, value, ip=None):
        if not isinstance(value, Hostname):
            value = Hostname(value, ip=ip)
        self._host_entries.append(value)

    def __contains__(self, value):
        for host_entry in self._host_entries:
            if host_entry == value:
                self._itr_current = 0
                return True
        return False

    def __len__(self):
        return len(self._host_entries)

    def __delitem__(self, index):
        del self._host_entries[index]

    def __iter__(self):
        return self

    def next(self):
        if self._itr_current > len(self._host_entries) - 1:
            self._itr_current = 0
            raise StopIteration
        else:
            self._itr_current += 1
            return self._host_entries[self._itr_current - 1]

    def __getitem__(self, index):
        return self._host_entries[index]

    def __str__(self):
        return 'HostList ({})'.format(len(self._host_entries))

    def __repr__(self):
        sample = list()
        for host in self._host_entries:
            if len(sample) > 2:
                break
            if host.fqdn is not None:
                sample.append(host.fqdn)
            else:
                sample.append(str(host.ip))
        output = ', '.join(sample)
        return '<HostList \'{}\'>'.format(output)


class Host(HostnameList):
    """ Represents all the names and IPs referring to the same host """

    def __init__(self, value, ip=None):
        super(Host, self).__init__()
        self._add(value, ip)
        self.display_name = value

    def __eq__(self, value):
        return self.__contains__(value)

    def add(self, value, ip=None):
        """ Merges a value with existing host entry values """
        if isinstance(value, basestring):
            if ip:
                value = Hostname(value, ip=ip)
            else:
                value = Hostname(value)

        if not isinstance(value, Hostname):
            raise TypeError('Can only add Hostname types')

        if value not in self._host_entries:
            raise ValueError('Host {} does not belong to {}'.format(value, self))
        # If existing Hostname matches the new one on all attributes, do nothing
        for entry in self._host_entries:
            if value.fqdn == entry.fqdn and entry.ip == value.ip:
                return True

        # If existing Hostname name matches but has no domain, add the domain to the existing Hostname
        for entry in self._host_entries:
            if entry.name == value.name and not entry.domain:
                entry.domain = value.domain
                break

        # If existing Hostname name matches but has no IP, add the IP to the existing Hostname
        for entry in self._host_entries:
            if value.name == entry.name and not entry.ip:
                entry.ip = value.ip

        # If existing Hostname name matches but the ip is different, add the new entry to the list
        existing_hostname = False
        for entry in self._host_entries:
            if entry.fqdn == value.fqdn and entry.ip != value.ip:
                existing_hostname = True
                break
        if existing_hostname:
            self._append(value)

        # New hostname on an existing IP
        existing_ip = False
        for entry in self._host_entries:
            if entry.ip == value.ip and entry.name != value.name:
                existing_ip = True
                break
        if existing_ip:
            self._append(value)

    @property
    def display_name(self):
        display = 'unknown'
        if hasattr(self, '_display_name'):
            existing = self.get(self._display_name)
            if existing:
                display = existing
            elif len(self):
                display = self._host_entries[0].fqdn
                self._display_name = display
        else:
            if len(self._host_entries):
                self._display_name = self._host_entries[0].fqdn
                display = self.get(self._display_name)
        return display

    @display_name.setter
    def display_name(self, value):
        if isinstance(value, Hostname):
            value = value.fqdn
        if '.' in value:
            value = Hostname._clean_fqdn(value)
            Validate.fqdn(value)
        else:
            value = Hostname._clean_name(value)
            Validate.host(value)
        if value not in self._host_entries:
            raise ValueError('Invalid display name \'{}\'. Value not found in the hostname list'.format(value))
        else:
            self._display_name = value

    def __str__(self):
        return 'Host {}'.format(self.display_name)

    def __repr__(self):
        return '<Host {}>'.format(self.display_name)
