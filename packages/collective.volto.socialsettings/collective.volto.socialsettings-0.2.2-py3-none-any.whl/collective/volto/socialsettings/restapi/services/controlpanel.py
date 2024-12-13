# -*- coding: utf-8 -*-
from collective.volto.socialsettings.interfaces import ISocialSettings
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class SocialSettingsControlpanel(RegistryConfigletPanel):
    schema = ISocialSettings
    configlet_id = "SocialSettings"
    configlet_category_id = "Products"
    schema_prefix = None
