# -*- coding: utf-8 -*-
from plone.app.standardtiles import PloneMessageFactory as _
from plone.app.standardtiles.existingcontent import IExistingContentTile
from zope import schema


class ILibraryCoreExistingContentTile(IExistingContentTile):
    view_template = schema.Choice(
        title=_("Display mode"),
        source=_("Available Content Views"),
        required=False,
    )
