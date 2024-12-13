# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import collective.volto.slimheader


class CollectiveVoltoSlimheaderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.slimheader)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.slimheader:default")


COLLECTIVE_VOLTO_SLIMHEADER_FIXTURE = CollectiveVoltoSlimheaderLayer()


COLLECTIVE_VOLTO_SLIMHEADER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_VOLTO_SLIMHEADER_FIXTURE,),
    name="CollectiveVoltoSlimheaderLayer:IntegrationTesting",
)


COLLECTIVE_VOLTO_SLIMHEADER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_VOLTO_SLIMHEADER_FIXTURE,),
    name="CollectiveVoltoSlimheaderLayer:FunctionalTesting",
)


COLLECTIVE_VOLTO_SLIMHEADER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_VOLTO_SLIMHEADER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveVoltoSlimheaderLayer:AcceptanceTesting",
)


class CollvectiveVoltoSlimheaderRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.restapi

        super().setUpZope(app, configurationContext)

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.slimheader)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.slimheader:default")


COLLECTIVE_VOLTO_SLIMHEADER_POLICY_API_FIXTURE = (
    CollvectiveVoltoSlimheaderRestApiLayer()
)
COLLECTIVE_VOLTO_SLIMHEADER_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_VOLTO_SLIMHEADER_POLICY_API_FIXTURE,),
    name="ProvinciaVaresePolicyRestApiLayer:Integration",
)

COLLECTIVE_VOLTO_SLIMHEADER_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_VOLTO_SLIMHEADER_POLICY_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ProvinciaVaresePolicyRestApiLayer:Functional",
)
