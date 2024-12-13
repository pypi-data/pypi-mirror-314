# -*- coding: utf-8 -*-
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface, implementer

from collective.volto.slimheader.interfaces import (
    ICollectiveVoltoSlimheaderLayer,
    ISlimHeader,
)


@adapter(Interface, ICollectiveVoltoSlimheaderLayer)
@implementer(ISlimHeader)
class SlimHeaderControlpanel(RegistryConfigletPanel):
    schema = ISlimHeader
    configlet_id = "Slimheader"
    configlet_category_id = "Products"
    schema_prefix = None
