# -*- coding: utf-8 -*-
from collective.volto.secondarymenu import _
from plone.restapi.controlpanels.interfaces import IControlpanel
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText
import json


class ISecondaryMenu(IControlpanel):
    secondary_menu_configuration = SourceText(
        title=_(
            "secondary_menu_configuration_label",
            default="Secondary menu configuration",
        ),
        description="",
        required=True,
        default=json.dumps([{"rootPath": "/", "items": []}]),
    )


class ICollectiveVoltoSecondaryMenuLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
