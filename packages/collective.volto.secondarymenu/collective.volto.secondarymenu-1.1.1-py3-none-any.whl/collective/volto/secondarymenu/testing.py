# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import collective.volto.secondarymenu
import plone.restapi


class VoltoSecondaryMenuLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.secondarymenu)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.secondarymenu:default")


VOLTO_SECONDARYMENU_FIXTURE = VoltoSecondaryMenuLayer()


VOLTO_SECONDARYMENU_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_SECONDARYMENU_FIXTURE,),
    name="VoltoSecondaryMenuLayer:IntegrationTesting",
)


VOLTO_SECONDARYMENU_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_SECONDARYMENU_FIXTURE,),
    name="VoltoSecondaryMenuLayer:FunctionalTesting",
)


class VoltoSecondaryMenuRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(VoltoSecondaryMenuRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.secondarymenu)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.secondarymenu:default")


VOLTO_SECONDARYMENU_API_FIXTURE = VoltoSecondaryMenuRestApiLayer()
VOLTO_SECONDARYMENU_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_SECONDARYMENU_API_FIXTURE,),
    name="VoltoSecondaryMenuRestApiLayer:Integration",
)

VOLTO_SECONDARYMENU_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_SECONDARYMENU_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VoltoSecondaryMenuRestApiLayer:Functional",
)
