# -*- coding: utf-8 -*-

import ipaddress


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
