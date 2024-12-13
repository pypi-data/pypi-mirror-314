# -*- coding: utf-8 -*-
from collective.volto.socialsettings.interfaces import ISocialSettings
from plone import api
import logging
import json

logger = logging.getLogger(__name__)


DEFAULT_PROFILE = "profile-collective.volto.socialsettings:default"


def update_profile(context, profile):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile)


def update_registry(context):
    update_profile(context, "plone.app.registry")


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def to_1001(context):
    """
    """
    records = json.dumps(
        api.portal.get_registry_record(
            "social_links", interface=ISocialSettings
        )
    )
    new_records = []
    for record in json.loads(records):
        values = record.split("|")
        if len(values) == 3:
            new_records.append(
                {"title": values[0], "icon": values[1], "url": values[2]}
            )
    update_registry(context)
    api.portal.set_registry_record(
        "social_links", json.dumps(new_records), interface=ISocialSettings
    )
