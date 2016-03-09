# -*- coding: utf-8 -*-

from ipaddress import IPv4Network
from nettool.ace import Ace as GenericAce


class Ace(GenericAce):

    @classmethod
    def _format_protocol(cls, source_transport, destination_transport):
        protocol = 'ip'
        if destination_transport is not None:
            protocol = destination_transport[0].type.lower()
            if protocol not in ('tcp', 'udp'):
                if source_transport is not None:
                    protocol = source_transport[0].type.lower()
        return protocol

    @classmethod
    def _format_protocol_name(cls, transport):
        protocol = 'ip'
        if transport is not None:
            if transport.name is not None:
                protocol = 'object-group {}'.format(transport.name)
            else:
                protocol = cls._format_protocol(transport.source, transport.destination)
        return protocol

    @classmethod
    def _format_transport(cls, transport_group):
        port = ''
        if transport_group is not None:
            if transport_group != transport_group.__class__():
                port = transport_group._port_string()
        return port

    @classmethod
    def _format_network(cls, network):
        if isinstance(network, IPv4Network):
            network = '{} {}'.format(str(network.network_address), str(network.netmask))
        return network

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

    def _grouped_ace(self, prefix, suffix):
        output = list()
        line = list()

        line.append(prefix)
        line.append(self._format_protocol_name(self.transport))

        for side in ('source', 'destination'):
            if getattr(self.network, side).name is not None:
                line.append('object-group {}'.format(getattr(self.network, side).name))
            else:
                line.append(self._format_network(getattr(self.network, side)[0]))
            if self.transport is not None and self.transport.name is None:
                if getattr(self.transport, side).name is not None:
                    line.append('object-group {}'.format(getattr(self.transport, side).name))
                else:
                    line.append(self._format_transport(getattr(self.transport, side)[0]))
        line.append(suffix)
        output.append(' '.join(line).replace('  ', ' ').strip())
        return output

    def show_run(self):
        return self._asa_print(expand=False)

    def show(self):
        return self._asa_print(expand=True)

    def _asa_print(self, expand=False):
        permission = 'permit'
        if not self.permit:
            permission = 'deny'
        prefix = permission

        suffix = ''
        if self.logging.level is not None:
            suffix = self.logging.name
        output = list()

        if self._is_grouped():
            output = self._grouped_ace(prefix, suffix)

        if self.transport is None:
            prefix = '{} ip'.format(prefix)
        if expand:
            for source_network, destination_network in self._iter_networks():
                for source_transport, destination_transport in self._iter_transport():
                    line = list()
                    line.append(prefix)
                    protocol = self._format_protocol(source_transport, destination_transport)
                    line.append(protocol)
                    line.append(self._format_network(source_network))
                    line.append(self._format_transport(source_transport, name=False))
                    line.append(self._format_network(destination_network))
                    line.append(self._format_transport(destination_transport, name=False))
                    line.append(suffix)
                    output.append(' '.join(line).replace('  ', ' ').strip())
        return '\n'.join(output)
