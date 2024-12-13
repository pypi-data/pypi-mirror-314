# -*- coding: utf-8 -*-
import json

from AccessControl.unauthorized import Unauthorized
from plone import api
from plone.restapi.interfaces import ISerializeToJson, ISerializeToJsonSummary
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter, getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer

from collective.volto.slimheader.interfaces import ISlimHeader

KEYS_WITH_URL = ["linkUrl", "navigationRoot", "showMoreLink"]


def serialize_data(json_data):
    if not json_data:
        return ""
    data = json.loads(json_data)
    for root in data:
        for tab in root.get("items", []):
            for key in KEYS_WITH_URL:
                value = tab.get(key, [])
                if value:
                    serialized = []
                    for uid in value:
                        try:
                            item = api.content.get(UID=uid)
                        except Unauthorized:
                            continue
                        if not item:
                            continue
                        summary = getMultiAdapter(
                            (item, getRequest()), ISerializeToJsonSummary
                        )()
                        if summary:
                            # serializer doesn't return uid
                            summary["UID"] = uid
                            serialized.append(summary)
                    tab[key] = serialized
    return json_compatible(data)


@implementer(ISerializeToJson)
@adapter(ISlimHeader)
class SlimHeaderControlpanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super().__call__()
        conf = json_data["data"].get("slimheader_configuration", "")
        if conf:
            json_data["data"]["slimheader_configuration"] = json.dumps(
                serialize_data(json_data=conf)
            )
        return json_data
