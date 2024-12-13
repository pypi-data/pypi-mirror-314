from collective.volto.gdprcookie.config import DEFAULT_SETTINGS
from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from collective.volto.gdprcookie.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class GDPRCookieSettingsTest(unittest.TestCase):
    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.page = api.content.create(
            container=self.portal, type="Document", title="A page"
        )
        commit()

    def test_route_exists(self):
        response = self.api_session.get("/@gdpr-cookie-settings")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def tearDown(self):
        self.api_session.close()

    def test_return_default_settings_if_not_customized(self):
        response = self.api_session.get("/@gdpr-cookie-settings")
        results = response.json()
        expected = {
            "show_icon": True,
            "cookie_version": "v1",
            "cookie_expires": 180,
        }
        expected.update(DEFAULT_SETTINGS)
        self.assertEqual(results, expected)

    def test_return_empty_value_if_banner_disabled(self):
        api.portal.set_registry_record(
            "banner_enabled", False, interface=IGDPRCookieSettings
        )
        commit()
        response = self.api_session.get("/@gdpr-cookie-settings")
        results = response.json()
        self.assertEqual(results, {})

    def test_return_only_technical_cookies_if_set(self):
        response = self.api_session.get("/@gdpr-cookie-settings")
        results = response.json()
        expected = {
            "show_icon": True,
            "cookie_version": "v1",
            "cookie_expires": 180,
        }
        expected.update(DEFAULT_SETTINGS)
        self.assertEqual(results, expected)

        api.portal.set_registry_record(
            "technical_cookies_only", True, interface=IGDPRCookieSettings
        )
        commit()

        response = self.api_session.get("/@gdpr-cookie-settings")
        results = response.json()
        expected = {
            "show_icon": True,
            "cookie_version": "v1",
            "cookie_expires": 180,
        }
        expected.update(DEFAULT_SETTINGS)
        del expected["profiling"]

        self.assertEqual(results, expected)
