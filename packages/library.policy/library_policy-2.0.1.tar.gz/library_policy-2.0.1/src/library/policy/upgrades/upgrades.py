# -*- coding: utf-8 -*-

from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.layout.layout import FacetedLayout
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from library.policy.utils import configure_faceted
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer

import os


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        "profile-library.policy:default",
    )


# silly : default_language = fr
# root and folders are fr-be !
def change_language(context):
    pl = api.portal.get_tool("portal_languages")
    default_language = pl.getDefaultLanguage()
    root = api.portal.get()
    brains = api.content.find(root)
    for brain in brains:
        obj = brain.getObject()
        if obj.language != default_language:
            obj.language = default_language
    root.language = default_language


def configure_faceted(context):
    pass


def upgrade_1004_to_1005(context):
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile("profile-collective.plausible:default")


def uninstall_z3cform_select2(context):
    installer = get_installer(context)
    installer.uninstall_product("collective.z3cform.select2")


def update_faceted_folders(context):
    brains = api.content.find(portal_type="Folder")
    for brain in brains:
        obj = brain.getObject()
        if not IFacetedNavigable.providedBy(obj):
            continue
        criteria_handler = ICriteria(obj)
        criteria = criteria_handler.criteria
        for criterion in criteria:
            if criterion.widget == "select2" or criterion.widget == "multiselect":
                criterion.update(widget="multiselect", placeholder=criterion.title)
        criteria_handler._update(criteria)


def update_faceted_layout(context):
    brains = api.content.find(object_provides=IFacetedNavigable)
    for brain in brains:
        obj = brain.getObject()
        layout = FacetedLayout(obj)
        layout.update_layout(layout="faceted-map")