# -*- coding: utf-8 -*-
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from eea.facetednavigation.layout.layout import FacetedLayout
from library.policy import _
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.i18n import translate
from zope.interface import implementer

import os


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "library.policy:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide unwanted products from site-creation and quickinstaller."""
        return [
            "library.policy.upgrades",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    add_taxonomies()
    add_stucture(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_taxonomies():
    current_lang = api.portal.get_default_language()[:2]
    # dossiers, patrimoine, villages, periodes
    data_dossiers = {
        "taxonomy": "dossiers",
        "field_title": translate(_("Dossiers"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_patrimoine = {
        "taxonomy": "patrimoine",
        "field_title": translate(_("Patrimoine"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_villages = {
        "taxonomy": "villages",
        "field_title": translate(_("Villages"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    data_periodes = {
        "taxonomy": "periodes",
        "field_title": translate(_("Periodes"), target_language=current_lang),
        "field_description": "",
        "default_language": "fr",
    }

    portal = api.portal.get()
    sm = portal.getSiteManager()

    dossiers_item = "collective.taxonomy.dossiers"
    patrimoine_item = "collective.taxonomy.patrimoine"
    villages_item = "collective.taxonomy.villages"
    periodes_item = "collective.taxonomy.periodes"
    utility_dossiers = sm.queryUtility(ITaxonomy, name=dossiers_item)
    utility_patrimoine = sm.queryUtility(ITaxonomy, name=patrimoine_item)
    utility_villages = sm.queryUtility(ITaxonomy, name=villages_item)
    utility_periodes = sm.queryUtility(ITaxonomy, name=periodes_item)
    if (
        utility_dossiers
        and utility_patrimoine
        and utility_villages
        and utility_periodes
    ):
        return

    create_taxonomy_object(data_dossiers)
    create_taxonomy_object(data_patrimoine)
    create_taxonomy_object(data_villages)
    create_taxonomy_object(data_periodes)


def add_stucture(portal):
    # Folder professionals
    if "explorer" not in portal:
        obj = create_content("Folder", _("explorer"), portal)
        subtyper = obj.restrictedTraverse("@@faceted_subtyper")
        subtyper.enable()        
        layout = FacetedLayout(obj)
        layout.update_layout(layout="faceted-map")
        _publish(obj)


def create_taxonomy_object(data_tax):
    taxonomy = registerTaxonomy(
        api.portal.get(),
        name=data_tax["taxonomy"],
        title=data_tax["field_title"],
        description=data_tax["field_description"],
        default_language=data_tax["default_language"],
    )

    del data_tax["taxonomy"]
    taxonomy.registerBehavior(**data_tax)


def create_content(type_content, title, parent):
    new_obj = api.content.create(type=type_content, title=title, container=parent)
    return new_obj


def _activate_dashboard_navigation(context, configuration=False, path=None):
    subtyper = context.restrictedTraverse("@@faceted_subtyper")
    if subtyper.is_faceted:
        return
    subtyper.enable()
    if configuration and path:
        config_path = os.path.dirname(__file__) + path
        with open(config_path, "rb") as config:
            context.unrestrictedTraverse("@@faceted_exportimport").import_xml(
                import_file=config
            )


def _publish(obj):
    if api.content.get_state(obj) != "published":
        api.content.transition(obj, transition="publish")
