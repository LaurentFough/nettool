# -*- coding: utf-8 -*-

from nettool.layer.network_envelope import NetworkEnvelope
from nettool.address.network_group import NetworkGroup


class NetworkLayer(NetworkEnvelope):
    _group_type = NetworkGroup
