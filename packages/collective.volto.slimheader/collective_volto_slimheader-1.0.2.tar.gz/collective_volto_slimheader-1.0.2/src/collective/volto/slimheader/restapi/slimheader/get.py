# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

from collective.volto.slimheader.interfaces import ISlimHeader

from ..serializers.slimheader import serialize_data


@implementer(IPublishTraverse)
class SlimHeaderGet(Service):
    def __init__(self, context, request):
        super().__init__(context, request)

    def reply(self):
        try:
            record = api.portal.get_registry_record(
                "slimheader_configuration",
                interface=ISlimHeader,
                default="",
            )
        except KeyError:
            return []
        if not record:
            return []
        return serialize_data(json_data=record)
