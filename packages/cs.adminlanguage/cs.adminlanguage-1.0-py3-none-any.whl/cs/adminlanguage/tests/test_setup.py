"""Setup tests for this package."""

from cs.adminlanguage.testing import CS_ADMINLANGUAGE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that cs.adminlanguage is properly installed."""

    layer = CS_ADMINLANGUAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if cs.adminlanguage is installed."""
        try:
            is_installed = self.installer.is_product_installed
        except AttributeError:
            is_installed = self.installer.isProductInstalled
        self.assertTrue(is_installed("cs.adminlanguage"))

    def test_browserlayer(self):
        """Test that ICsAdminlanguageLayer is registered."""
        from cs.adminlanguage.interfaces import ICsAdminlanguageLayer
        from plone.browserlayer import utils

        self.assertIn(ICsAdminlanguageLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CS_ADMINLANGUAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
            self.installer.uninstall_product("cs.adminlanguage")
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
            self.installer.uninstallProducts(["cs.adminlanguage"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if cs.adminlanguage is cleanly uninstalled."""
        try:
            is_installed = self.installer.is_product_installed
        except AttributeError:
            is_installed = self.installer.isProductInstalled
        self.assertFalse(is_installed("cs.adminlanguage"))

    def test_browserlayer_removed(self):
        """Test that ICsAdminlanguageLayer is removed."""
        from cs.adminlanguage.interfaces import ICsAdminlanguageLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICsAdminlanguageLayer, utils.registered_layers())
