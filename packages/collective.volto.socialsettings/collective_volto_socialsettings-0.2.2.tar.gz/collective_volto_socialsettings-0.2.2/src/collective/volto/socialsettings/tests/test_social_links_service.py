# -*- coding: utf-8 -*-
from collective.volto.socialsettings.testing import (
    VOLTO_SOCIALSETTINGS_API_FUNCTIONAL_TESTING,
)
from collective.volto.socialsettings.interfaces import ISocialSettings
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import json
import unittest


class SocialLinksServiceTest(unittest.TestCase):

    layer = VOLTO_SOCIALSETTINGS_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_route_exists(self):
        response = self.api_session.get("/@social-links")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def test_return_empty_list_if_not_set(self):
        response = self.api_session.get("/@social-links")

        results = response.json()
        self.assertEqual(results, [])

    def test_right_data(self):
        test_data = [
            {"title": "foo", "icon": "bar", "url": "baz"},
            {"title": "xxx", "icon": "yyy", "url": "zzz"},
        ]
        api.portal.set_registry_record(
            "social_links", json.dumps(test_data), interface=ISocialSettings
        )
        commit()
        response = self.api_session.get("/@social-links")
        results = response.json()
        self.assertEqual(len(results), 2)
        self.assertEqual(
            results[0], {"title": "foo", "icon": "bar", "url": "baz"}
        )
        self.assertEqual(
            results[1], {"title": "xxx", "icon": "yyy", "url": "zzz"}
        )
