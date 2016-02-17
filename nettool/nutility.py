# -*- coding: utf-8 -*-

import re
import ipaddress

from ipv4address import IPv4Address


class NUtility(object):
    wildcards = [ipaddress.IPv4Interface(unicode('0.0.0.0/{0}'.format(x))).network.hostmask.exploded for x in range(0, 33)]
    netmasks = [ipaddress.IPv4Interface(unicode('255.255.255.255/{0}'.format(x))).network.network_address.exploded for x in range(0, 33)]

    class validate(object):
        @staticmethod
        def netmask(netmask):
            return netmask in NUtility.netmasks

        @staticmethod
        def wildcard(wildcard):
            return wildcard in NUtility.wildcards

        @staticmethod
        def prefix(prefix):
            return prefix in range(0, 33)

        @staticmethod
        def _host_base_checks(value):
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
        def host(host):
            try:
                NUtility.validate._host_base_checks(host)
                if len(host) < 1:
                    raise ValueError("'{}' host too short. Hostname be between 1-63 characters long".format(host))
                if len(host) > 63:
                    raise ValueError("'{}' host too long. Hostname be between 1-63 characters long".format(host))
            except ValueError:
                return False
            return True

        @staticmethod
        def hostname(value):
            try:
                if len(value) > 253:
                    raise ValueError("'{}' is too long. FQDN must be less than 254 characters".format(value))
                for part in value.split('.'):
                    if not NUtility.validate.host(part):
                        return False
            except ValueError:
                return False
            return True

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
