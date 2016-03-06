# -*- coding: utf-8 -*-

from nettool.address.transport_address_builder import TransportAddressBuilder
from nettool.address.transport_group import TransportGroup
from nettool.address.transport_address import TransportAddress
from nettool.layer.transport_layer import TransportLayer
from nettool.utilities import raise_type_exception


class TransportLayerBuilder(object):

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, (basestring, int)) or isinstance(text, bool):
            raise_type_exception(text, (str, unicode), 'build with')
        return True

    @classmethod
    def _validate_ports(cls, text, original_text):
        for port in text.split():
            if not port.isdigit():
                cls._invalid_builder(original_text)

    @staticmethod
    def _clean_text(text):
        text = str(text)
        replacements = (('-', ' '), ('  ', ' '))
        for match, replacement in replacements:
            text = text.replace(match, replacement)
        return text.lower().strip()

    @staticmethod
    def _invalid_builder(text):
        raise ValueError('Unable to build a transport layer from \'{}\''.format(text))

    @classmethod
    def _normalize(cls, text, original_text):
        cls._validate_ports(text, original_text)
        values = text.split()
        default_range = '{}-{}'.format(TransportAddress._min, TransportAddress._max)
        # 22 --> 1-65535 22-22
        if len(values) is 1:
            text = '{0} {1}-{1}'.format(default_range, values[0])
        # 1 2 --> 1 65535 1 2
        elif len(values) is 2:
            text = '{} {}-{}'.format(default_range, values[0], values[1])
        # 1 2 --> 1 65535 1 2
        elif len(values) is 4:
            text = '{}-{} {}-{}'.format(values[0], values[1], values[2], values[3])
        else:
            cls._invalid_builder(original_text)
        return text

    @classmethod
    def build(cls, text):
        if isinstance(text, TransportLayer):
            return text
        elif text is None:
            return TransportLayer()
        original_text = text
        cls._validate_text(text)
        text = cls._clean_text(text)
        protocol_cls, text = TransportAddressBuilder._extract_protocol(text)
        text = cls._normalize(text, original_text)
        source, destination = text.split()
        source_group = TransportGroup()
        source_group.add(protocol_cls.from_string(source))
        destination_group = TransportGroup()
        destination_group.add(protocol_cls.from_string(destination))
        return TransportLayer(source=source_group, destination=destination_group)
