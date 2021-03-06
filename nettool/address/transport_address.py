# -*- coding: utf-8 -*-

from nettool.nettest import NetTest as nu
from nettool.utilities import raise_type_exception


class TransportAddress(object):
    _address_name = 'TCP/UDP'
    type = 'TCP/UDP'
    _min = 1
    _max = 65535

    def __init__(self, low=None, high=None):
        self._low = None
        self._high = None
        self.low = low
        self.high = high

    @classmethod
    def from_string(cls, value):
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, basestring):
            if value.isdigit():
                return cls(value)
            value = cls._clean_port_string(value)
            ports = value.split()
            if len(ports) == 2:
                low, high = ports
                valid = nu.validate._port(low)
                valid = valid and nu.validate._port(high)
                if valid:
                    low = int(low)
                    high = int(high)
                    if low > high:
                        address = cls(low=high, high=low)
                    else:
                        address = cls(low=low, high=high)
                    return address
        message = 'Unsupported string initialization format \'{}\''
        message = message.format(value)
        raise ValueError(message)

    @classmethod
    def _clean_port_string(cls, value):
        if not isinstance(value, basestring):
            raise_type_exception(value, (str, unicode), 'build with')
        return value.replace('-', ' ').replace('  ', ' ').strip()

    @property
    def low(self):
        port = self._low
        if port is None:
            port = self._high
            if self._high is None:
                port = self._min
        return port

    def _validate_port(self, port):
        return nu.validate._port(port, raise_exception=True)

    @low.setter
    def low(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._high is None:
                self._high = self._max
            elif self.high < value:
                message = 'The low port {} cannot be higher than the high port {}'
                message = message.format(value, self.high)
                raise ValueError(message)
        self._low = value

    @property
    def high(self):
        port = self._high
        if port is None:
            port = self._low
            if self._low is None:
                port = self._max
        return port

    @high.setter
    def high(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._low is None:
                self._low = self._min
            elif self.low > value:
                message = 'The high port {} cannot be lower than the low port {}'
                message = message.format(value, self.low)
                raise ValueError(message)
        self._high = value

    def _port_string(self):
        if self.low == self.high:
            port = str(self.low)
        else:
            port = '{}-{}'.format(self.low, self.high)
        return port

    def __repr__(self):
        port = self._port_string()
        return '<{} {}>'.format(self.__class__.__name__, port)

    def __str__(self):
        port = self._port_string()
        # if port == '{}-{}'.format(self._min, self._max):
        #     return ''
        return '{} {}'.format(self._address_name, port)

    def __eq__(self, key):
        test01 = isinstance(key, self.__class__)
        return test01 and self.low == key.low and self.high == key.high

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if isinstance(key, basestring):
            if key.isdigit():
                key = int(key)
            else:
                key = self.from_string(key)
        if isinstance(key, self.__class__):
            return self.low <= key.low and self.high >= key.high
        elif issubclass(key.__class__, TransportAddress):
            return False
        elif isinstance(key, int):
            nu.validate._port(key, raise_exception=True)
            return self.low <= key and self.high >= key
        raise_type_exception(key, (self.__class__, ), 'test membership of')
