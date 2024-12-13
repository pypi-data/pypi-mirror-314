from collective.volto.gdprcookie.config import DEFAULT_SETTINGS
from collective.volto.gdprcookie.testing import RESTAPI_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import unittest


class TestExpansion(unittest.TestCase):
    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_expansion_visible(self):
        response = self.api_session.get(self.portal_url)
        result = response.json()
        self.assertIn("gdpr-cookie-settings", result["@components"])

    def test_expansion_not_expanded_by_default(self):
        response = self.api_session.get(self.portal_url)
        result = response.json()
        self.assertEqual(
            result["@components"]["gdpr-cookie-settings"],
            {"@id": f"{self.portal_url}/@gdpr-cookie-settings"},
        )

    def test_expansion_expanded_if_passed_parameter(self):
        response = self.api_session.get(
            f"{self.portal_url}?expand=gdpr-cookie-settings"
        )
        result = response.json()
        data = result["@components"]["gdpr-cookie-settings"]

        expected = {
            "show_icon": True,
            "cookie_version": "v1",
            "cookie_expires": 180,
        }
        expected.update(DEFAULT_SETTINGS)
        self.assertEqual(data, expected)
