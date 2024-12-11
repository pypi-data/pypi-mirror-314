# -*- coding: utf-8 -*-
from collective.faceted.map.browser.map import MapView
from plone.api.portal import get_registry_record

import json


class FacetedMapView(MapView):
    """Faceted map view"""

    def get_images(self, obj):
        if getattr(obj, "image", None) is None:
            return ""
        image_field_id = "image"
        images = obj.restrictedTraverse('@@images')
        image_mini = images.scale(image_field_id,"mini")
        return image_mini.url

    def map_configuration(self):
        """Returns global map configuration from registry"""
        map_layers = get_registry_record("geolocation.map_layers") or []
        config = {
            "fullscreencontrol": get_registry_record("geolocation.fullscreen_control"),
            "locatecontrol": get_registry_record("geolocation.locate_control"),
            "zoomcontrol": get_registry_record("geolocation.zoom_control"),
            "minimap": get_registry_record("geolocation.show_minimap"),
            "addmarker": get_registry_record("geolocation.show_add_marker"),
            "geosearch": get_registry_record("geolocation.show_geosearch"),
            "geosearch_provider": get_registry_record("geolocation.geosearch_provider"),
            "default_map_layer": get_registry_record("geolocation.default_map_layer"),
            "map_layers": [
                {"title": "Titre", "id": layer}
                for layer in map_layers
            ],
            "latitude": get_registry_record("geolocation.default_latitude"),
            "longitude": get_registry_record("geolocation.default_longitude"),
        }
        return json.dumps(config)
