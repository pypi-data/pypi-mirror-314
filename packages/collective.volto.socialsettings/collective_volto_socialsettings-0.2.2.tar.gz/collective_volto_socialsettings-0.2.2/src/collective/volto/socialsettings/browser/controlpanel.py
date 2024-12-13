# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.volto.socialsettings.interfaces import ISocialSettings
from collective.volto.socialsettings import _


class SocialSettingsForm(controlpanel.RegistryEditForm):

    schema = ISocialSettings
    label = _("social_settings_label", default=u"Social Settings")
    description = u"Settings for social links"


class SocialSettings(controlpanel.ControlPanelFormWrapper):
    form = SocialSettingsForm
