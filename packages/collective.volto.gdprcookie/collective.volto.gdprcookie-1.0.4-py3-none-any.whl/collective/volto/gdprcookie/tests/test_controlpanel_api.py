from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from collective.volto.gdprcookie.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import json
import unittest


class GDPRCookieControlpanelTest(unittest.TestCase):
    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.controlpanel_url = "/@controlpanels/gdpr-cookie-settings"

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.page = api.content.create(
            container=self.portal, type="Document", title="A page"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def get_record_value(self):
        record = api.portal.get_registry_record(
            "settings",
            interface=IGDPRCookieSettings,
            default="",
        )
        if not record:
            return {}
        return json.loads(record)

    def test_controlpanel_exists(self):
        response = self.api_session.get(self.controlpanel_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def test_controlpanel_listed(self):
        response = self.api_session.get("/@controlpanels")

        titles = [x.get("title") for x in response.json()]
        self.assertIn("GDPR Cookie Settings", titles)
