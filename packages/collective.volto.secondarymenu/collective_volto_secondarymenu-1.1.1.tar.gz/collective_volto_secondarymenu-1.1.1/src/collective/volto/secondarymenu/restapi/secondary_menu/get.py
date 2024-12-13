# -*- coding: utf-8 -*-
from collective.volto.secondarymenu.interfaces import ISecondaryMenu
from collective.volto.secondarymenu.restapi.serializer.secondary_menu import (
    serialize_data,
)
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class SecondaryMenuGet(Service):
    def __init__(self, context, request):
        super(SecondaryMenuGet, self).__init__(context, request)

    def reply(self):
        try:
            record = api.portal.get_registry_record(
                "secondary_menu_configuration",
                interface=ISecondaryMenu,
                default="",
            )
        except KeyError:
            return []
        if not record:
            return []
        return serialize_data(json_data=record)
