# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

from collective.volto.slimheader.testing import (  # noqa: E501
    COLLECTIVE_VOLTO_SLIMHEADER_INTEGRATION_TESTING,
)

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.volto.slimheader is properly installed."""

    layer = COLLECTIVE_VOLTO_SLIMHEADER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.volto.slimheader is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.volto.slimheader")
        )

    def test_browserlayer(self):
        """Test that ICollectiveVoltoSlimheaderLayer is registered."""
        from plone.browserlayer import utils

        from collective.volto.slimheader.interfaces import (
            ICollectiveVoltoSlimheaderLayer,
        )

        self.assertIn(ICollectiveVoltoSlimheaderLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_VOLTO_SLIMHEADER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.volto.slimheader")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.volto.slimheader is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.volto.slimheader")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveVoltoSlimheaderLayer is removed."""
        from plone.browserlayer import utils

        from collective.volto.slimheader.interfaces import (
            ICollectiveVoltoSlimheaderLayer,
        )

        self.assertNotIn(ICollectiveVoltoSlimheaderLayer, utils.registered_layers())
