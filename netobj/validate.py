# -*- coding: utf-8 -*-

import re
from ipv4address import IPv4Address


class Validate(object):

    @staticmethod
    def _host_base(value):
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
    def ip(value):
        if not isinstance(value, IPv4Address):
            IPv4Address(value)

    @staticmethod
    def host(value):
        Validate._host_base(value)
        if len(value) < 1:
            raise ValueError("'{}' hostname too short. Hostname be between 1-63 characters long".format(value))
        if len(value) > 63:
            raise ValueError("'{}' hostname too long. Hostname be between 1-63 characters long".format(value))

    @staticmethod
    def fqdn(value):
        if len(value) > 253:
            raise ValueError("'{}' is too long. FQDN must be less than 254 characters".format(value))
