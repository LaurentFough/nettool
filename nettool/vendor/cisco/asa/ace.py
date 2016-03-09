# -*- coding: utf-8 -*-

from ipaddress import IPv4Network
from nettool.ace import Ace as GenericAce


class AsaAddress(object):
    valid_protocols = ('ip', 'tcp', 'udp')

    @classmethod
    def protocol(cls, source_transport, destination_transport):
        if source_transport is None and destination_transport is None:
            protocol = 'ip'
        else:
            if destination_transport is not None:
                protocol = destination_transport.type.lower()
                if protocol not in cls.valid_protocols:
                    if source_transport is not None:
                        protocol = source_transport.type.lower()
        if protocol == 'tcp/udp':
            protocol = 'ip'
        if protocol not in cls.valid_protocols:
            message = 'Invalid protocol {}. Must be: {}'
            message = message.format(protocol, ', '.join(cls.valid_protocols))
            raise ValueError(message)
        return protocol

    @classmethod
    def protocol_group(cls, transport):
        protocol = 'ip'
        if transport is not None:
            if transport.name is not None:
                protocol = 'object-group {}'.format(transport.name)
            else:
                protocol = cls.protocol(transport.source[0], transport.destination[0])
        return protocol

    @classmethod
    def transport(cls, transport):
        port = ''
        if transport is not None:
            if transport != transport.__class__():
                port = transport._port_string()
                port = port.replace('-', ' ')
                if len(port.split()) == 2:
                    port = 'range {}'.format(port)
                else:
                    port = 'eq {}'.format(port)
        return port

    @classmethod
    def transport_group(cls, transport):
        if transport.name is not None:
            transport = 'object-group {}'.format(transport.name)
        else:
            transport = cls.transport(transport[0])
        return transport

    @classmethod
    def network(cls, network):
        if isinstance(network, IPv4Network):
            network = '{} {}'.format(str(network.network_address), str(network.netmask))
        return network

    @classmethod
    def network_group(cls, network):
        if network.name is None:
            network = cls.network(network[0])
        else:
            network = 'object-group {}'.format(network.name)
        return network


class Ace(GenericAce):

    def show_run(self):
        return self._ace_print(expand=False)

    def show(self):
        return self._ace_print(expand=True)

    def _is_grouped(self):
        """ Does the ACE consist of groupings? """
        names = list()
        if self.transport is not None:
            names.append(self.transport.name)
            names.append(self.transport.source.name)
            names.append(self.transport.destination.name)
        names.append(self.network.source.name)
        names.append(self.network.destination.name)
        return any(names)

    def _collapsed_print(self, prefix, suffix):
        output = list()
        line = list()

        line.append(prefix)
        line.append(AsaAddress.protocol_group(self.transport))

        for side in ('source', 'destination'):
            line.append(AsaAddress.network_group(getattr(self.network, side)))
            if self.transport is not None and self.transport.name is None:
                line.append(AsaAddress.transport_group(getattr(self.transport, side)))
        line.append(suffix)
        output.append(' '.join(line).replace('  ', ' ').strip())
        return output

    def _ace_print(self, expand=False):
        permission = 'permit'
        if not self.permit:
            permission = 'deny'
        prefix = permission

        suffix = ''
        if self.logging.level is not None:
            suffix = self.logging.name
        output = list()

        if not expand and self._is_grouped():
            output = self._collapsed_print(prefix, suffix)

        if expand or (not expand and not self._is_grouped()):
            for source_network, destination_network in self._iter_networks():
                for source_transport, destination_transport in self._iter_transport():
                    line = list()
                    line.append(prefix)
                    line.append(AsaAddress.protocol(source_transport, destination_transport))
                    line.append(AsaAddress.network(source_network))
                    line.append(AsaAddress.transport(source_transport))
                    line.append(AsaAddress.network(destination_network))
                    line.append(AsaAddress.transport(destination_transport))
                    line.append(suffix)
                    output.append(' '.join(line).replace('  ', ' ').strip())
        return '\n'.join(output)
