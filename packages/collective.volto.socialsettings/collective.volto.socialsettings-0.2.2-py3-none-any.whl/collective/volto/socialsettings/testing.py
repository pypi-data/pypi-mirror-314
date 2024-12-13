# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import collective.volto.socialsettings
import plone.restapi


class VoltoSocialSettingsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.socialsettings)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.socialsettings:default")


VOLTO_SOCIALSETTINGS_FIXTURE = VoltoSocialSettingsLayer()


VOLTO_SOCIALSETTINGS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_SOCIALSETTINGS_FIXTURE,),
    name="VoltoSocialSettingsLayer:IntegrationTesting",
)


VOLTO_SOCIALSETTINGS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_SOCIALSETTINGS_FIXTURE,),
    name="VoltoSocialSettingsLayer:FunctionalTesting",
)


class VoltoSocialSettingsRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(VoltoSocialSettingsRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.socialsettings)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.volto.socialsettings:default")


VOLTO_SOCIALSETTINGS_API_FIXTURE = VoltoSocialSettingsRestApiLayer()
VOLTO_SOCIALSETTINGS_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_SOCIALSETTINGS_API_FIXTURE,),
    name="VoltoSocialSettingsRestApiLayer:Integration",
)

VOLTO_SOCIALSETTINGS_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_SOCIALSETTINGS_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VoltoSocialSettingsRestApiLayer:Functional",
)
