# -*- coding: utf-8 -*-

import ipaddress


class NUtility(object):
    wildcards = [ipaddress.IPv4Interface(unicode('0.0.0.0/{0}'.format(x))).network.hostmask.exploded for x in range(0, 33)]
    netmasks = [ipaddress.IPv4Interface(unicode('255.255.255.255/{0}'.format(x))).network.network_address.exploded for x in range(0, 33)]

    class convert(object):
        class netmask(object):
            @staticmethod
            def wildcard(netmask):
                if netmask not in NUtility.netmasks:
                    raise ValueError(u'Invalid netmask {}'.format(netmask))
                return NUtility.wildcards[NUtility.netmasks.index(netmask)]

        class wildcard(object):
            @staticmethod
            def netmask(wildcard):
                if wildcard not in NUtility.wildcards:
                    raise ValueError(u'Invalid wildcard {}'.format(wildcard))
                return NUtility.netmasks[NUtility.wildcards.index(wildcard)]
