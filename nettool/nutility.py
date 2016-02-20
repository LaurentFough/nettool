# -*- coding: utf-8 -*-

import re
import ipaddress

from ipv4address import IPv4Address
from unidecode import unidecode


class NUtility(object):
    wildcards = [ipaddress.IPv4Interface(
        unicode('0.0.0.0/{}'.format(x))).network.hostmask.exploded for x in range(0, 33)]
    netmasks = [ipaddress.IPv4Interface(
        unicode('255.255.255.255/{}'.format(x)))
        .network.network_address.exploded for x in range(0, 33)]

    class validate(object):
        @staticmethod
        def _port(port, raise_exception=False):
            if isinstance(port, basestring) and port.isdigit():
                port = int(port)
            elif type(port) is not int:
                if raise_exception:
                    message = 'Invalid port type \'{}\'.'
                    raise TypeError(message.format(type(port)))
                return False
            valid = port > 0 and port < 65536
            if not valid and raise_exception:
                message = 'Invalid port number \'{}\'. Must be between {}-{}'
                raise ValueError(message.format(port, 1, 65535))
            return valid

        @staticmethod
        def tcp_port(port, raise_exception=False):
            return NUtility.validate._port(port, raise_exception=raise_exception)

        @staticmethod
        def udp_port(port, raise_exception=False):
            return NUtility.validate._port(port, raise_exception=raise_exception)

        @staticmethod
        def netmask(netmask, raise_exception=False):
            valid = netmask in NUtility.netmasks
            if not valid and raise_exception:
                raise ValueError('Invalid netmask {}'.format(netmask))
            return valid

        @staticmethod
        def wildcard(wildcard, raise_exception=False):
            valid = wildcard in NUtility.wildcards
            if not valid and raise_exception:
                raise ValueError('Invalid wildcard {}'.format(wildcard))
            return valid

        @staticmethod
        def prefix(prefix, raise_exception=False):
            valid = prefix in range(0, 33)
            if not valid and raise_exception:
                raise ValueError('Invalid prefix {}'.format(prefix))
            return valid

        @staticmethod
        def ip(value, raise_exception=False):
            if not isinstance(value, basestring):
                if raise_exception:
                    raise ValueError('Invalid type \'{}\''.format(type(value)))
                return False
            try:
                if not isinstance(value, IPv4Address):
                    IPv4Address(value)
            except (ValueError, TypeError):
                if raise_exception:
                    raise
                return False
            return True

        @staticmethod
        def network(value, raise_exception=False):
            if not isinstance(value, basestring):
                if raise_exception:
                    raise ValueError('Invalid type \'{}\''.format(type(value)))
                return False
            try:
                value = unicode(value)
                ipaddress.IPv4Interface(value)
            except (ValueError, TypeError):
                if raise_exception:
                    raise
                return False
            return True

        @staticmethod
        def _host_base_checks(value, raise_exception=False):
            if not isinstance(value, basestring):
                if raise_exception:
                    raise ValueError('Invalid type \'{}\''.format(type(value)))
                return False
            try:
                if isinstance(value, unicode):
                    str(value)
                else:
                    unicode(value, encoding='ascii')
            except UnicodeDecodeError as e:
                value = unicode(value, 'utf-8')
                position = re.search(r'in position (\d+):', str(e)).group(1)
                invalid_character = value[int(position)]
                error_message = u"'{}' invalid character '{}'. Must use ASCII characters"
                error_message = error_message.format(value, invalid_character)
                if raise_exception:
                    raise ValueError(error_message)
                return False
            invalid_character_match = re.search(r'([^0-9a-z\-])', value.lower())
            if invalid_character_match:
                if raise_exception:
                    message = "'{}' invalid character \'{}\'."
                    message = message.format(value, invalid_character_match.group(1))
                    raise ValueError(message)
                return False
            return True

        @staticmethod
        def host(value, raise_exception=False):
            if not isinstance(value, basestring):
                if raise_exception:
                    raise ValueError('Invalid type \'{}\''.format(type(value)))
                return False
            if not NUtility.validate._host_base_checks(value, raise_exception=raise_exception):
                return False
            if len(value) < 1:
                if raise_exception:
                    message = "'{}' host too short. Hostname be between 1-63 characters long"
                    message = message.format(value)
                    raise ValueError(message)
                return False
            if len(value) > 63:
                if raise_exception:
                    message = "'{}' host too long. Hostname be between 1-63 characters long"
                    message = message.format(value)
                    raise ValueError(message)
                return False
            return True

        @staticmethod
        def hostname(value, raise_exception=False):
            if not isinstance(value, basestring):
                if raise_exception:
                    raise ValueError('Invalid type \'{}\''.format(type(value)))
                return False
            if len(value) > 253:
                if raise_exception:
                    message = "'{}' is too long. FQDN must be less than 254 characters"
                    message = message.format(value)
                    raise ValueError(message)
                return False
            for domain_level in value.split('.'):
                if not NUtility.validate.host(domain_level):
                    if raise_exception:
                        message = "Inalid domain level name '{}' in hostname '{}'."
                        message = message.format(domain_level, value)
                        raise ValueError(message)
                    return False
            return True

    class coerce(object):

        class string(object):

            @staticmethod
            def _base_host_coerce(value):
                replacements = ((' ', '-'), ('(', '-'), (')', '-'), ('_', '-'),
                                ('/', '-'), ('\\', '-'), ('--', '-'), )
                for before, after in replacements:
                    value = value.replace(before, after)
                strips = ('-', '.')
                for strip in strips:
                    value = value.strip(strip)
                value = value.strip()
                value = value.lower()
                value = unicode(value)
                value = unidecode(value)
                return value

            @staticmethod
            def host(value):
                value = NUtility.coerce.string._base_host_coerce(value)
                NUtility.validate.host(value, raise_exception=True)
                return value

            @staticmethod
            def hostname(value):
                value = NUtility.coerce.string._base_host_coerce(value)
                NUtility.validate.hostname(value, raise_exception=True)
                return value

    class convert(object):

        class prefix(object):
            @staticmethod
            def netmask(prefix):
                if not NUtility.validate.prefix(prefix):
                    raise ValueError(u'Invalid prefix length \'{}\''.format(prefix))
                return NUtility.netmasks[prefix]

            @staticmethod
            def wildcard(prefix):
                if not NUtility.validate.prefix(prefix):
                    raise ValueError(u'Invalid prefix length \'{}\''.format(prefix))
                return NUtility.wildcards[prefix]

        class netmask(object):
            @staticmethod
            def wildcard(netmask):
                if not NUtility.validate.netmask(netmask):
                    raise ValueError(u'Invalid netmask \'{}\''.format(netmask))
                return NUtility.wildcards[NUtility.netmasks.index(netmask)]

            @staticmethod
            def prefix(netmask):
                if not NUtility.validate.netmask(netmask):
                    raise ValueError(u'Invalid netmask \'{}\''.format(netmask))
                return NUtility.netmasks.index(netmask)

        class wildcard(object):
            @staticmethod
            def netmask(wildcard):
                if not NUtility.validate.wildcard(wildcard):
                    raise ValueError(u'Invalid wildcard \'{}\''.format(wildcard))
                return NUtility.netmasks[NUtility.wildcards.index(wildcard)]

            @staticmethod
            def prefix(wildcard):
                if not NUtility.validate.wildcard(wildcard):
                    raise ValueError(u'Invalid wildcard \'{}\''.format(wildcard))
                return NUtility.wildcards.index(wildcard)
