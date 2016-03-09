# -*- coding: utf-8 -*-

from nettool.acl import Acl as GenericAcl


class Acl(GenericAcl):

    def __init__(self, name):
        super(Acl, self).__init__(name=name, default_permit=False)
