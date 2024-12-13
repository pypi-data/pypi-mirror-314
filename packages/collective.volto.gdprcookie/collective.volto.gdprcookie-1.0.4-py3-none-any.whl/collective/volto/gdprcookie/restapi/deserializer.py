from collective.volto.gdprcookie.interfaces import IGDPRCookieSettingsControlpanel
from collective.volto.gdprcookie.restapi import parse_gdpr_blocks
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import ControlpanelDeserializeFromJson
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer


@implementer(IDeserializeFromJson)
@adapter(IGDPRCookieSettingsControlpanel)
class GDPRCookieSettingsDeserializeFromJson(ControlpanelDeserializeFromJson):
    def __call__(self):
        """
        Convert json data into a string
        """
        super().__call__()

        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(self.schema, prefix=self.schema_prefix)
        errors = []

        gdpr_cookie_settings = req.get("gdpr_cookie_settings", {})
        if not gdpr_cookie_settings:
            errors.append(
                {
                    "message": "Missing data",
                    "field": "gdpr_cookie_settings",
                }
            )
            raise BadRequest(errors)
        gdpr_cookie_settings = parse_gdpr_blocks(
            context=self.context,
            data=gdpr_cookie_settings,
            transformer_interface=IBlockFieldDeserializationTransformer,
        )
        try:
            setattr(proxy, "gdpr_cookie_settings", gdpr_cookie_settings)
        except ValueError as e:
            errors.append(
                {
                    "message": str(e),
                    "field": "gdpr_cookie_settings",
                    "error": e,
                }
            )

        if errors:
            raise BadRequest(errors)
