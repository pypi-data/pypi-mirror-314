# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel

from collective.volto.slimheader import _
from collective.volto.slimheader.interfaces import ISlimHeader


class SlimHeaderForm(controlpanel.RegistryEditForm):

    schema = ISlimHeader
    label = _("slimheader_settings_label", default="Slim Header Settings")
    description = ""


class SlimHeader(controlpanel.ControlPanelFormWrapper):
    form = SlimHeaderForm
