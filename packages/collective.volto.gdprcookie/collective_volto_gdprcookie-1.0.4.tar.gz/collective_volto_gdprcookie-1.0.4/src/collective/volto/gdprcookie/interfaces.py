from collective.volto.gdprcookie import _
from collective.volto.gdprcookie.config import DEFAULT_SETTINGS
from plone.restapi.controlpanels import IControlpanel
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Bool
from zope.schema import Int
from zope.schema import SourceText
from zope.schema import TextLine

import json


class ICollectiveVoltoGdprcookieLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IGDPRCookieSettingsControlpanel(IControlpanel):
    """ """


class IGDPRCookieSettings(Interface):
    banner_enabled = Bool(
        title=_("banner_enabled_label", default="Banner enabled"),
        description=_(
            "banner_enabled_help",
            default="If selected, the cookie banner will be prompt to the users.",
        ),
        default=True,
    )
    show_icon = Bool(
        title=_("show_icon_label", default="Show banner preferences icon"),
        description=_(
            "show_icon_help",
            default="If selected, the preferences icon will be shown.",
        ),
        default=True,
    )
    cookie_version = TextLine(
        title=_("cookie_version_label", default="Cookie version"),
        description=_(
            "cookie_version_help",
            default="Set the version number for the technical cookie that will store user preferences. Changing this value will invalidate previous user preferences and force them to re-accept them.",
        ),
        default="v1",
    )
    cookie_expires = Int(
        title=_("cookie_expires_label", default="Cookie expires"),
        description=_(
            "cookie_expires_help",
            default="Set the expire date of banner cookie in days.",
        ),
        default=180,
    )
    technical_cookies_only = Bool(
        title=_("technical_cookies_only_label", default="Technical cookies only"),
        description=_(
            "technical_cookies_only_help",
            default="Select this to enable only the technical cookies part of the banner.",
        ),
        default=False,
        required=False,
    )

    gdpr_cookie_settings = SourceText(
        title=_("gdpr_cookie_settings_label", default="Cookie banner configuration"),
        description="",
        required=True,
        default=json.dumps(DEFAULT_SETTINGS),
    )
