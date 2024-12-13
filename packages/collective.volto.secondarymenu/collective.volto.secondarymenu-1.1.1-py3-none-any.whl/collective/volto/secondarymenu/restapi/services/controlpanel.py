# -*- coding: utf-8 -*-
from collective.volto.secondarymenu.interfaces import (
    ICollectiveVoltoSecondaryMenuLayer,
    ISecondaryMenu,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, ICollectiveVoltoSecondaryMenuLayer)
@implementer(ISecondaryMenu)
class SecondaryMenuControlpanel(RegistryConfigletPanel):
    schema = ISecondaryMenu
    configlet_id = "SecondaryMenu"
    configlet_category_id = "Products"
    schema_prefix = None
