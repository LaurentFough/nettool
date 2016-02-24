# -*- coding: utf-8 -*-

from nettool.nutility import NUtility as nu


class TransportAddress(object):
    _min = 1
    _max = 65535

    def __init__(self, low=None, high=None):
        self._low = None
        self._high = None
        self.low = low
        self.high = high

    @staticmethod
    def from_string(value):
        if isinstance(value, int):
            return TransportAddress(value)
        if isinstance(value, basestring):
            if value.isdigit():
                return TransportAddress(value)
            value = TransportAddress._clean_port_string(value)
            ports = value.split()
            if len(ports) == 2:
                low, high = ports
                valid = nu.validate._port(low)
                valid = valid and nu.validate._port(high)
                if valid:
                    low = int(low)
                    high = int(high)
                    if low > high:
                        address = TransportAddress(low=high, high=low)
                    else:
                        address = TransportAddress(low=low, high=high)
                    return address
        message = 'Unsupported string initialization format \'{}\''
        message = message.format(value)
        raise ValueError(message)

    @staticmethod
    def _clean_port_string(value):
        if not isinstance(value, basestring):
            message = 'Type {} unsupported. Must use a string'
            message = message.format(type(value).__name__)
            raise TypeError(message)
        return value.replace('-', ' ').replace('  ', ' ').strip()

    @property
    def low(self):
        port = self._low
        if port is None:
            port = self._high
            if self._high is None:
                port = TransportAddress._min
        return port

    def _validate_port(self, port):
        return nu.validate._port(port, raise_exception=True)

    @low.setter
    def low(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._high is None:
                self._high = TransportAddress._max
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
                port = TransportAddress._max
        return port

    @high.setter
    def high(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._low is None:
                self._low = TransportAddress._min
            elif self.low > value:
                message = 'The high port {} cannot be lower than the low port {}'
                message = message.format(value, self.low)
                raise ValueError(message)
        self._high = value

    def _port_range_string(self):
        if self.low == self.high:
            port = self.low
        else:
            port = '{}-{}'.format(self.low, self.high)
        return port

    def __repr__(self):
        port = self._port_range_string()
        return '<{} {}>'.format(self.__class__.__name__, port)

    def __str__(self):
        port = self._port_range_string()
        return 'Port {}'.format(port)

    def __eq__(self, key):
        return self.low == key.low and self.high == key.high

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if isinstance(key, basestring):
            if key.isdigit():
                key = int(key)
            else:
                key = TransportAddress.from_string(key)
        if isinstance(key, TransportAddress):
            return self.low <= key.low and self.high >= key.high
        elif isinstance(key, int):
            nu.validate._port(key, raise_exception=True)
            return self.low <= key and self.high >= key
        class_name = self.__class__.__name__
        message = 'Cannot test if {} contains {} types.'
        message = message.format(class_name, type(key).__name__)
        raise TypeError(message)
