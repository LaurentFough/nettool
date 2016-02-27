# -*- coding: utf-8 -*-

from nettool.hostname import Hostname


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
