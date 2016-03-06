# -*- coding: utf-8 -*-

from nettool.address.transport_address import TransportAddress
from nettool.address.tcp_address import TcpAddress
from nettool.address.udp_address import UdpAddress
from nettool.utilities import raise_type_exception


class TransportAddressBuilder(object):
    _instance_aliases = {
        'tcp': TcpAddress,
        'udp': UdpAddress,
    }

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, (basestring, int)) or isinstance(text, bool):
            raise_type_exception(text, (str, unicode), 'build with')
        return True

    @staticmethod
    def _clean_text(text):
        return str(text).replace('-', ' ')

    @staticmethod
    def _invalid_builder(text):
        raise ValueError('Unable to build a transport address from \'{}\''.format(text))

    @classmethod
    def _extract_protocol(cls, text):
        protocol = TransportAddress
        parts = text.split()
        if len(parts) > 0 and not parts[0].isdigit():
            protocol_string = parts.pop(0).lower()
            if protocol_string in cls._instance_aliases.keys():
                protocol = cls._instance_aliases[protocol_string]
            else:
                cls._invalid_builder(text)
        text = ' '.join(parts)
        return (protocol, text)

    @classmethod
    def build(cls, text):
        if isinstance(text, (TransportAddress, )):
            return text
        cls._validate_text(text)
        text = cls._clean_text(text)
        protocol, text = cls._extract_protocol(text)
        return protocol.from_string(text)
