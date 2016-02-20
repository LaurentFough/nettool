# -*- coding: utf-8 -*-

from nettool.nutility import NUtility as nu


class TransportLayer(object):
    _min = 1
    _max = 65535

    def __init__(self, low=None, high=None):
        self._low = None
        self._high = None
        self.low = low
        self.high = high

    @property
    def low(self):
        port = self._low
        if port is None:
            port = self._high
            if self._high is None:
                port = TransportLayer._min
        return port

    def _validate_port(self, port):
        return nu.validate._port(port, raise_exception=True)

    @low.setter
    def low(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._high is None:
                self._high = TransportLayer._max
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
                port = TransportLayer._max
        return port

    @high.setter
    def high(self, value):
        if value is not None:
            self._validate_port(value)
            value = int(value)
            if self._low is None:
                self._low = TransportLayer._min
            elif self.low > value:
                message = 'The high port {} cannot be lower than the low port {}'
                message = message.format(value, self.low)
                raise ValueError(message)
        self._high = value

    def __repr__(self):
        if self.low == self.high:
            port = self.low
        else:
            port = '{}-{}'.format(self.low, self.high)
        return '<{} {}>'.format(self.__class__.__name__, port)

    def __eq__(self, key):
        return self.low == key.low and self.high == key.high

    def __ne__(self, key):
        return not self.__eq__(key)

    def __contains__(self, key):
        if isinstance(key, TransportLayer):
            return self.low <= key.low and self.high >= key.high
        elif isinstance(key, int) or (isinstance(key, basestring) and key.isdigit()):
            nu.validate._port(key, raise_exception=True)
            key = int(key)
            return self.low <= key and self.high >= key
        class_name = self.__class__.__name__
        message = 'Cannot test if {} contains {} types.'
        message = message.format(class_name, type(key).__name__)
        raise TypeError(message)
