# -*- coding: utf-8 -*-
from collective.volto.socialsettings import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText


class ISocialSettings(Interface):
    """ Interface for social settings controlpanel """

    social_links = SourceText(
        title=_("social_links_label", default="Social links"),
        description=_(
            "social_links_help",
            default="Insert a list of values for social links.",
        ),
        default="",
    )


class ICollectiveVoltoSocialsettingsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
