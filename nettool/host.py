# -*- coding: utf-8 -*-

from nettool.hostname import Hostname
from nettool.hostname_list import HostnameList
from nettool.nettest import NetTest as nu


class Host(HostnameList):
    """ Represents all the names and IPs referring to the same host """

    def __init__(self, value, ip=None):
        super(Host, self).__init__()
        self._add(value, ip)

    def __eq__(self, value):
        return self.__contains__(value)

    def add(self, value, ip=None):
        """ Merges a value with existing host entry values """
        if isinstance(value, basestring):
            value = Hostname(value, ip=ip)

        if not isinstance(value, Hostname):
            raise TypeError('Can only add Hostname types')

        if value not in self._host_entries:
            raise ValueError('Host {} does not belong to {}'.format(value, self))
        # If existing Hostname matches the new one on all attributes, do nothing
        for entry in self._host_entries:
            if value.fqdn == entry.fqdn and entry.ip == value.ip:
                return True

        # If existing Hostname name matches but has no domain, add the domain
        #  to the existing Hostname
        for entry in self._host_entries:
            if entry.name == value.name and not entry.domain:
                entry.domain = value.domain
                break

        # If existing Hostname name matches but has no IP, add the IP to the existing Hostname
        if nu.validate.ip(value.ip):
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
    def display_hostname(self):
        display = 'unknown'
        for hostname in self._host_entries:
            if display == 'unknown':
                display = hostname.fqdn
            elif len(hostname.fqdn) > display:
                display = hostname.fqdn
        return display

    def __str__(self):
        return 'Host {}'.format(self.display_hostname)

    def __repr__(self):
        return '<Host {}>'.format(self.display_hostname)
