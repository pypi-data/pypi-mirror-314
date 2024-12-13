# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import library.policy


class LibraryPolicyLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=library.policy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "library.policy:default")


LIBRARY_POLICY_FIXTURE = LibraryPolicyLayer()


LIBRARY_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LIBRARY_POLICY_FIXTURE,),
    name="LibraryPolicyLayer:IntegrationTesting",
)


LIBRARY_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIBRARY_POLICY_FIXTURE,),
    name="LibraryPolicyLayer:FunctionalTesting",
)


LIBRARY_POLICY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LIBRARY_POLICY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="LibraryPolicyLayer:AcceptanceTesting",
)
