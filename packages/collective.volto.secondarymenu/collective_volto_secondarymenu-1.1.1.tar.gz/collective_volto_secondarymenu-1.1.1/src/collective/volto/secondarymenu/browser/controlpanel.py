# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.volto.secondarymenu.interfaces import ISecondaryMenu
from collective.volto.secondarymenu import _


class SecondaryMenuForm(controlpanel.RegistryEditForm):

    schema = ISecondaryMenu
    label = _(
        "secondary_menu_settings_label", default=u"Secondary Menu Settings"
    )
    description = u""


class SecondaryMenu(controlpanel.ControlPanelFormWrapper):
    form = SecondaryMenuForm
