from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import collective.volto.gdprcookie
import plone.restapi


class TestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.gdprcookie)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.gdprcookie:default")


FIXTURE = TestLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="VoltoGDPRCookieRestApiLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="VoltoGDPRCookieRestApiLayer:FunctionalTesting",
)

RESTAPI_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="VoltoGDPRCookieRestApiLayer:RestAPITesting",
)
