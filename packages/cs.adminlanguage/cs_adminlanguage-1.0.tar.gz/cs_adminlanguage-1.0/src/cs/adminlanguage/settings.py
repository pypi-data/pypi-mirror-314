from cs.adminlanguage.messagefactory import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """Define settings data structure"""

    adminLanguage = schema.TextLine(
        title=_("Editor language"),
        description=_(
            "Type two letter language code and admins always use this language"
        ),
        required=False,
    )


class SettingsControlPanelForm(RegistryEditForm):
    schema = ISettings
    schema_prefix = "admin_language"
    label = _("Language Admin Settings")


SettingsPanelView = layout.wrap_form(SettingsControlPanelForm, ControlPanelFormWrapper)
