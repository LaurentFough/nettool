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
    def protocol_name(cls, transport):
        protocol = 'ip'
        if transport is not None:
            if transport.name is not None:
                protocol = 'object-group {}'.format(transport.name)
            else:
                protocol = cls.protocol(transport.source[0],
                                        transport.destination[0])
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
    def transport_name(cls, transport, side):
        output = ''
        if transport is not None and transport.name is None:
            transport_side = getattr(transport, side)
            if transport_side.name is not None:
                output = 'object-group {}'.format(transport_side.name)
            else:
                output = cls.transport(transport_side[0])
        return output

    @classmethod
    def network(cls, network):
        if isinstance(network, IPv4Network):
            network = '{} {}'.format(str(network.network_address),
                                     str(network.netmask))
        return network

    @classmethod
    def network_name(cls, network):
        if network.name is None:
            network = cls.network(network[0])
        else:
            network = 'object-group {}'.format(network.name)
        return network


class Ace(GenericAce):

    def show_run(self):
        return self._print(expand=False)

    def show(self):
        return self._print(expand=True)

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

    def _print_named(self, permission, logging):

        protocol = AsaAddress.protocol_name(self.transport)
        source_network = AsaAddress.network_name(self.network.source)
        destination_network = AsaAddress.network_name(self.network.destination)
        source_transport = AsaAddress.transport_name(self.transport, 'source')
        destination_transport = AsaAddress.transport_name(self.transport, 'destination')

        line = list()
        line.append(permission)
        line.append(protocol)
        line.append(source_network)
        line.append(source_transport)
        line.append(destination_network)
        line.append(destination_transport)
        line.append(logging)

        output = list()
        output.append(' '.join(line).replace('  ', ' ').strip())
        return output

    def _print(self, expand=False):
        permission = self._print_permission()
        logging = str(self.logging)

        output = list()
        if not expand and self._is_grouped():
            output = self._print_named(permission, logging)

        if expand or (not expand and not self._is_grouped()):
            for source_net, destination_net in self._iter_networks():
                for source_port, destination_port in self._iter_transport():
                    protocol = AsaAddress.protocol(source_port, destination_port)

                    source_network = AsaAddress.network(source_net)
                    destination_network = AsaAddress.network(destination_net)

                    source_transport = AsaAddress.transport(source_port)
                    destination_transport = AsaAddress.transport(destination_port)

                    line = list()
                    line.append(permission)
                    line.append(protocol)
                    line.append(source_network)
                    line.append(source_transport)
                    line.append(destination_network)
                    line.append(destination_transport)
                    line.append(logging)
                    output.append(' '.join(line).replace('  ', ' ').strip())
        return '\n'.join(output)
