# -*- coding: utf-8 -*-

import re
import ipaddress

from unidecode import unidecode


class NetTest(object):
    wildcards = [ipaddress.IPv4Interface(
        unicode('0.0.0.0/{}'.format(x))).network.hostmask.exploded for x in range(0, 33)]
    netmasks = [ipaddress.IPv4Interface(
        unicode('255.255.255.255/{}'.format(x)))
        .network.network_address.exploded for x in range(0, 33)]

    class validate(object):
        """ Network validation """
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

        @classmethod
        def tcp_port(cls, port, raise_exception=False):
            """ Layer 4 TCP port validation """
            return cls._port(port, raise_exception=raise_exception)

        @classmethod
        def udp_port(cls, port, raise_exception=False):
            """ Layer 4 UDP port validation """
            return cls._port(port, raise_exception=raise_exception)

        @staticmethod
        def netmask(netmask, raise_exception=False):
            """ Network subnet mask validation """
            valid = netmask in NetTest.netmasks
            if not valid and raise_exception:
                raise ValueError('Invalid netmask {}'.format(netmask))
            return valid

        @staticmethod
        def wildcard(wildcard, raise_exception=False):
            """ Network wildcard mask validation """
            valid = wildcard in NetTest.wildcards
            if not valid and raise_exception:
                raise ValueError('Invalid wildcard {}'.format(wildcard))
            return valid

        @staticmethod
        def prefix(prefix, raise_exception=False):
            """ CIDR prefix length validation """
            valid = prefix in range(0, 33)
            if not valid and raise_exception:
                raise ValueError('Invalid prefix {}'.format(prefix))
            return valid

        @classmethod
        def _get_network_object(cls, network):
            cls.ip(network, raise_exception=True) or cls.ip(network, raise_exception=True)
            network = NetTest.convert.string.cidr(network)
            network = ipaddress.IPv4Interface(network).network
            return network

        @classmethod
        def is_subnet(cls, subnet, supernet):
            """ Network is a subnet of the given supernet """
            subnet = cls._get_network_object(subnet)
            supernet = cls._get_network_object(supernet)
            return subnet.subnet_of(supernet)

        @classmethod
        def ip(cls, value, raise_exception=False):
            """ IP address validation """
            if cls.network(value):
                value = NetTest.convert.string.cidr(value)
                if value.endswith('/32'):
                    value = value.split('/')[0]
                else:
                    return False
            if not isinstance(value, basestring):
                if raise_exception:
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
                return False
            else:
                value = unicode(value)
            try:
                ipaddress.IPv4Address(value)
            except (ValueError, TypeError):
                if raise_exception:
                    raise
                return False
            return True

        @classmethod
        def network(cls, value, raise_exception=False):
            """ Network address validation """
            if not isinstance(value, basestring):
                if raise_exception:
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
                return False
            terms = value.split()
            if len(terms) is 2:
                if cls.ip(terms[0]):
                    if cls.netmask(terms[1]):
                        terms[1] = NetTest.convert.netmask.prefix(terms[1])
                    elif cls.wildcard(terms[1]):
                        terms[1] = NetTest.convert.wildcard.prefix(terms[1])
                    terms[1] = unicode(terms[1])
                value = u'/'.join(terms)
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
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
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
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
                return False
            if not NetTest.validate._host_base_checks(value, raise_exception=raise_exception):
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
            """ DNS hostname validation """
            if not isinstance(value, basestring):
                if raise_exception:
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
                return False
            if len(value) > 253:
                if raise_exception:
                    message = "'{}' is too long. FQDN must be less than 254 characters"
                    message = message.format(value)
                    raise ValueError(message)
                return False
            for domain_level in value.split('.'):
                if not NetTest.validate.host(domain_level):
                    if raise_exception:
                        message = "Inalid domain level name '{}' in hostname '{}'."
                        message = message.format(domain_level, value)
                        raise ValueError(message)
                    return False
            return True

    class convert(object):

        class string(object):

            @staticmethod
            def _base_host_convert(value):
                replacements = ((' ', '-'), ('(', '-'), (')', '-'), ('_', '-'),
                                ('/', '-'), ('\\', '-'), (':', '-'), ('--', '-'), )
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

            @classmethod
            def host(cls, value):
                value = cls._base_host_convert(value)
                cls.validate.host(value, raise_exception=True)
                return value

            @classmethod
            def _standardize_cidr_format(cls, value):
                if not isinstance(value, basestring):
                    raise TypeError('Invalid type \'{}\''.format(type(value)))
                terms = value.split()
                if len(terms) is 2:
                    if NetTest.validate.ip(terms[0]):
                        if NetTest.validate.netmask(terms[1]):
                            terms[1] = NetTest.convert.netmask.prefix(terms[1])
                        elif NetTest.validate.wildcard(terms[1]):
                            terms[1] = NetTest.convert.wildcard.prefix(terms[1])
                        terms[1] = unicode(terms[1])
                    value = u'/'.join(terms)
                if '/' not in value:
                    value = value + '/32'
                value = unicode(value)
                return value

            @classmethod
            def cidr(cls, value):
                """ Convert a string to a network CIDR """
                value = cls._standardize_cidr_format(value)
                value = ipaddress.IPv4Interface(value).network.exploded
                return value

            @classmethod
            def network_longest_match(cls, value):
                """ Convert a string to a network address longest prefix match """
                network = cls.network_address(value)
                broadcast = cls.broadcast_address(value)
                common = ''
                for i1, i2 in zip(network, broadcast):
                    if i1 == i2:
                        common = ''.join([common, i1])
                    else:
                        break
                return common

            @staticmethod
            def network_address(value):
                """ Convert a string to a network IP """
                value = NetTest.convert.string.cidr(value)
                return ipaddress.IPv4Network(value).network_address.exploded

            @staticmethod
            def broadcast_address(value):
                """ Convert a string to a broadcast IP """
                value = NetTest.convert.string.cidr(value)
                return ipaddress.IPv4Network(value).broadcast_address.exploded

            @classmethod
            def ip(cls, value):
                """ String to IP conversion """
                value = cls._standardize_cidr_format(value)
                NetTest.validate.ip(value, raise_exception=True)
                value = value.split('/')[0]
                return value

            @classmethod
            def hostname(cls, value):
                """ Convert a string to DNS hostname """
                value = cls._base_host_convert(value)
                NetTest.validate.hostname(value, raise_exception=True)
                return value

        class prefix(object):
            """ CIDR prefix conversions """

            @staticmethod
            def netmask(prefix):
                """ CIDR prefix to subnet mask conversion """
                if not NetTest.validate.prefix(prefix):
                    raise ValueError(u'Invalid prefix length \'{}\''.format(prefix))
                return NetTest.netmasks[prefix]

            @staticmethod
            def wildcard(prefix):
                """ CIDR prefix to wildcard mask conversion """
                if not NetTest.validate.prefix(prefix):
                    raise ValueError(u'Invalid prefix length \'{}\''.format(prefix))
                return NetTest.wildcards[prefix]

        class netmask(object):
            """ Network subnet mask conversions """
            @staticmethod
            def wildcard(netmask):
                """ Network subnet mask to wildcard mask conversion """
                if not NetTest.validate.netmask(netmask):
                    raise ValueError(u'Invalid netmask \'{}\''.format(netmask))
                return NetTest.wildcards[NetTest.netmasks.index(netmask)]

            @staticmethod
            def prefix(netmask):
                """ Network subnet mask to CIDR prefix conversion """
                if not NetTest.validate.netmask(netmask):
                    raise ValueError(u'Invalid netmask \'{}\''.format(netmask))
                return NetTest.netmasks.index(netmask)

        class wildcard(object):
            """ Network wildcard mask conversions """
            @staticmethod
            def netmask(wildcard):
                """ Network wildcard mask to netmask conversion """
                if not NetTest.validate.wildcard(wildcard):
                    raise ValueError(u'Invalid wildcard \'{}\''.format(wildcard))
                return NetTest.netmasks[NetTest.wildcards.index(wildcard)]

            @staticmethod
            def prefix(wildcard):
                """ Network wildcard mask to cidr prefix conversion """
                if not NetTest.validate.wildcard(wildcard):
                    raise ValueError(u'Invalid wildcard \'{}\''.format(wildcard))
                return NetTest.wildcards.index(wildcard)
