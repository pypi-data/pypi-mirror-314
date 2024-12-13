# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

import json

from plone.restapi.controlpanels.interfaces import IControlpanel
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText

from collective.volto.slimheader import _


class ISlimHeader(IControlpanel):
    slimheader_configuration = SourceText(
        title=_(
            "slimheader_configuration_label",
            default="Slim Header Configuration",
        ),
        description="",
        required=True,
        default=json.dumps([{"rootPath": "/", "items": []}]),
    )


class ICollectiveVoltoSlimheaderLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
