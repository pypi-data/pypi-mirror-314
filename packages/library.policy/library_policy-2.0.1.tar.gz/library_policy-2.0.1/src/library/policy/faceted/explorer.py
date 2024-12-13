# -*- coding: utf-8 -*-

from collective.faceted.map import _
from collective.faceted.map.browser.map import MapView
from plone import api
from zope.i18n import translate

import json


class ExplorerView(MapView):
    @property
    def map_configuration(self):
        map_layers = api.portal.get_registry_record("geolocation.map_layers") or []
        config = {
            "fullscreencontrol": api.portal.get_registry_record(
                "geolocation.fullscreen_control", default=True
            ),
            "locatecontrol": api.portal.get_registry_record(
                "geolocation.locate_control", default=True
            ),
            "zoomcontrol": api.portal.get_registry_record(
                "geolocation.zoom_control", default=True
            ),
            "minimap": api.portal.get_registry_record(
                "geolocation.show_minimap", default=True
            ),
            "addmarker": api.portal.get_registry_record(
                "geolocation.show_add_marker", default=False
            ),
            "geosearch": api.portal.get_registry_record(
                "geolocation.show_geosearch", default=False
            ),
            "geosearch_provider": api.portal.get_registry_record(
                "geolocation.geosearch_provider", default=[]
            ),
            "default_map_layer": api.portal.get_registry_record(
                "geolocation.default_map_layer", default=[]
            ),
            "latitude": api.portal.get_registry_record(
                "geolocation.default_latitude", default=0.0
            ),
            "longitude": api.portal.get_registry_record(
                "geolocation.default_longitude", default=0.0
            ),
            "map_layers": [
                {
                    "title": translate(_(map_layer), context=self.request),
                    "id": map_layer,
                }
                for map_layer in map_layers
            ],
            "useCluster": False,
        }
        return json.dumps(config)
