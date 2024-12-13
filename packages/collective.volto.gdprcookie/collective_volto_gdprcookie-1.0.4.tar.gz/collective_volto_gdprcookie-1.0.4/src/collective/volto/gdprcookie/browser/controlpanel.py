from collective.volto.gdprcookie import _
from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from plone.app.registry.browser import controlpanel


class GDPRCookieForm(controlpanel.RegistryEditForm):
    schema = IGDPRCookieSettings
    label = _("gdpr_cookie_settings_controlpanel_label", default="GDPR Cookie Settings")


class GDPRCookieControlPanel(controlpanel.ControlPanelFormWrapper):
    form = GDPRCookieForm
