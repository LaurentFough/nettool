# -*- coding: utf-8 -*-


class ProtocolLayer(object):
    _default_name = 'ip'
    _valid_protocols = (
        'ip',
        'tcp',
        'udp',
        'icmp',
    )

    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def _clean_name(name):
        if name is None:
            name = ProtocolLayer._default_name
        else:
            if not isinstance(name, basestring):
                raise ValueError('Invalid type \'{}\' for protocol'.format(type(name)))
            if name not in ProtocolLayer._valid_protocols:
                raise ValueError('Invalid protocol \'{}\''.format(name))
        return name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = ProtocolLayer._clean_name(value)
