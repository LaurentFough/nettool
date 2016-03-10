# -*- coding: utf-8 -*-

from nettool.hostname import Hostname
from nettool.hostname_list import HostnameList
from nettool.utilities import raise_type_exception


class Host(HostnameList):
    """ Represents all the names and IPs referring to the same host """

    def __init__(self, value, ip=None):
        super(Host, self).__init__()
        self._add(value, ip)

    def __eq__(self, value):
        return self.__contains__(value)

    def _update_hostname_attributes(self, hostname):
        """ Update exisiting hostnames without an attribute with the new hosts' attribute """
        for attribute in ('domain', 'ip'):
            for self_host in self._host_entries:
                if hostname.name == self_host.name:
                    if not getattr(self_host, attribute):
                        setattr(self_host, attribute, getattr(hostname, attribute))

    def _add_hostname_new_ip(self, hostname):
        for entry in self._host_entries:
            if entry.fqdn == hostname.fqdn and entry.ip != hostname.ip:
                self._append(hostname)
                return

    def _add_ip_new_hostname(self, hostname):
        for entry in self._host_entries:
            if entry.ip == hostname.ip and entry.name != hostname.name:
                self._append(hostname)
                return

    def add(self, value, ip=None):
        """ Merges a value with existing host entry values """
        if isinstance(value, basestring):
            value = Hostname(value, ip=ip)

        if not isinstance(value, Hostname):
            raise_type_exception(value, (Hostname, ), 'add')

        if value not in self._host_entries:
            raise ValueError('Host {} does not belong to {}'.format(value, self))

        self._update_hostname_attributes(value)

        for entry in self._host_entries:
            if value.fqdn == entry.fqdn:
                if entry.ip == value.ip:
                    # Full match found. Do nothing
                    return

        self._add_hostname_new_ip(value)
        self._add_ip_new_hostname(value)

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
