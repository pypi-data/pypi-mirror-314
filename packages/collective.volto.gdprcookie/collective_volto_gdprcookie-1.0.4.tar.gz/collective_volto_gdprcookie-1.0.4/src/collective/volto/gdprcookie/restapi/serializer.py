from collective.volto.gdprcookie.interfaces import IGDPRCookieSettingsControlpanel
from collective.volto.gdprcookie.restapi import parse_gdpr_blocks
from plone import api
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from zope.component import adapter
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


@implementer(ISerializeToJson)
@adapter(IGDPRCookieSettingsControlpanel)
class GDPRCookieSettingsSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super().__call__()
        gdpr_cookie_settings = json_data["data"].get("gdpr_cookie_settings", "{}")
        json_data["data"]["gdpr_cookie_settings"] = parse_gdpr_blocks(
            context=api.portal.get(),
            data=gdpr_cookie_settings,
            transformer_interface=IBlockFieldSerializationTransformer,
        )
        return json_data
