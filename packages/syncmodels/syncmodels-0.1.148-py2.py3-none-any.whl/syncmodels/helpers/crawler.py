"""Crawler Helpers"""

import re
from datetime import datetime
from typing import List, Dict

from agptools.helpers import DATE, build_uri
from agptools.containers import walk

from ..definitions import ID_KEY, ORG_KEY
from ..crud import parse_duri
from ..model.geojson import BaseGeometry, Point


class SortKeyFinder:
    WANTED_TYPES = tuple([datetime])
    DATE_KEYS = r"|".join(
        [
            ".*date",
            "time",
            "year",
            # 'ts',
            "sent",
            "rewiew",
            "update",
            "entity_ts",
        ]
    )
    DATE_REGEXP = re.compile(DATE_KEYS)

    SORT_KEY_CACHE = {}

    @classmethod
    def register(cls, kind, sort_key):
        cls.SORT_KEY_CACHE[kind] = sort_key

    @classmethod
    def get(cls, kind):
        return cls.SORT_KEY_CACHE.get(kind)

    @classmethod
    def differentiable(cls, item):
        """return a convenience key for sorting element that can be sustracted"""
        _range = item[1]
        assert len(_range) == 2
        # x = _range[0] - 1 * (_range[1] - _range[0])
        x = _range[0]
        return x

    @classmethod
    def find_sort_key(cls, stream: List[Dict], kind=None):
        """
        Try to figure-out which is the best key for sortering data stream
        in order to feed the storage as close as possible to the order that
        events must appear in storage for real-time observation and KPI calculation
        """
        universe = {}
        assert isinstance(stream, List), "maybe find_sort_key( [data] ) instead?"
        for key, value in walk(stream):
            _key = key[1:]
            if _key and cls.DATE_REGEXP.match(str(_key[-1])):
                value = DATE(value)
            if isinstance(value, cls.WANTED_TYPES):
                klass = value.__class__
                candidates = universe.setdefault(klass, {})
                candidates.setdefault(_key, []).append(value)

        # discard any non-fully-present keys
        for klass, candidates in list(universe.items()):
            for key, samples in list(candidates.items()):
                if len(samples) == len(stream):
                    candidates[key] = min(samples), max(samples)
                else:
                    candidates.pop(key)

            if candidates:
                candidates = list([k, v] for k, v in candidates.items())
                candidates.sort(key=cls.differentiable)
                universe[klass] = candidates[0]
            else:
                universe.pop(klass)
        for type_ in cls.WANTED_TYPES:
            candidate = universe.get(type_)
            if candidate:
                sort_key = candidate[0]
                # example: sort_key = ('sent',)
                if isinstance(sort_key, str):
                    sort_key = tuple([sort_key])
                return sort_key
        return tuple([])


class GeojsonManager:
    @classmethod
    def geo_uri(cls, data):
        "returns the uri of a related object"
        for candidate in [ORG_KEY, ID_KEY]:
            if _sid := data.get(candidate):
                _sid = parse_duri(_sid)
                if _sid["fscheme"] != "test":

                    _sid["path"] = "/{thing}/geo".format_map(_sid)
                    fquid = build_uri(**_sid)
                    return fquid

    @classmethod
    def centroid(cls, geojson: BaseGeometry):
        """Generic Centroid calculation for any GeoJSON type"""
        coordinates = list(geojson["coordinates"])
        geo_type = geojson["type"]
        if geo_type in ("Point",):
            return geojson

        # use
        _coordinates = {}
        for key, value in walk(coordinates):
            if len(key) > 0:
                idx = key[-1]
                if isinstance(idx, int) and isinstance(value, float):
                    _coordinates.setdefault(idx, []).append(value)

        # # assume order is: lng, lat
        # translation = ['lng', 'lat']
        # centroid = {
        #     translation[key]: sum(value) / len(value)
        #     for key, value in _coordinates.items()
        # }
        keys = list(_coordinates.keys())
        keys.sort()
        centroid = [sum(_coordinates[key]) / len(_coordinates[key]) for key in keys]
        centroid = Point(coordinates=centroid)
        return centroid
