from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from collective.volto.gdprcookie.restapi import parse_gdpr_blocks
from plone import api
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import json


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class GDPRCookieSettings:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "gdpr-cookie-settings": {
                "@id": f"{self.context.absolute_url()}/@gdpr-cookie-settings"
            }
        }
        if not expand:
            return result

        result["gdpr-cookie-settings"] = self.get_data()
        return result

    def get_field_value(self, field):
        """
        Return value from registry
        """
        try:
            return (
                api.portal.get_registry_record(field, interface=IGDPRCookieSettings)
                or None
            )
        except KeyError:
            # product not installed
            return None

    def get_gdpr_cookies_value(self):
        gdpr_cookies_settings = self.get_field_value(field="gdpr_cookie_settings")
        data = parse_gdpr_blocks(
            context=self.context,
            data=gdpr_cookies_settings,
            transformer_interface=IBlockFieldSerializationTransformer,
        )
        return json.loads(data)

    def get_data(self):
        """
        Return settings
        """
        enabled = self.get_field_value(field="banner_enabled")
        if not enabled:
            return {}
        show_icon = self.get_field_value(field="show_icon")
        technical_cookies_only = self.get_field_value(field="technical_cookies_only")
        gdpr_cookie_settings = self.get_gdpr_cookies_value()
        data = {
            "show_icon": show_icon,
            "cookie_version": self.get_field_value(field="cookie_version"),
            "cookie_expires": self.get_field_value(field="cookie_expires"),
        }
        if technical_cookies_only and "profiling" in gdpr_cookie_settings:
            del gdpr_cookie_settings["profiling"]
        data.update(gdpr_cookie_settings)
        return data


class GDPRCookieSettingsGet(Service):
    def reply(self):
        data = GDPRCookieSettings(self.context, self.request)
        return data(expand=True)["gdpr-cookie-settings"]
