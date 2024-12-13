from collective.volto.gdprcookie.interfaces import ICollectiveVoltoGdprcookieLayer
from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from collective.volto.gdprcookie.interfaces import IGDPRCookieSettingsControlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, ICollectiveVoltoGdprcookieLayer)
@implementer(IGDPRCookieSettingsControlpanel)
class GDPRCookieSettingsControlpanel(RegistryConfigletPanel):
    schema = IGDPRCookieSettings
    configlet_id = "GDPRCookieSettings"
    configlet_category_id = "Products"
    schema_prefix = None
