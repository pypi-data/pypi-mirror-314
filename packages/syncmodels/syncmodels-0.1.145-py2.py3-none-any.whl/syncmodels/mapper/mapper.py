"""
Mappers transform plain dict to another dict
converting key and values.

Classes definition are inspired on pydantic

"""

import re
import sys
import traceback
import inspect
import itertools
from typing import Dict, Union, _GenericAlias

from math import isnan
from datetime import timedelta
from dateutil.parser import parse

from glom import glom, T, Coalesce, SKIP
from pydantic import ValidationError

# ------------------------------------------------
# Converter functions
# ------------------------------------------------
from agptools.helpers import (
    BOOL,
    DATE,
    DURATION,
    FLOAT,
    I,
    INT,
    STRIP,
    TEXT,
    STR,
)

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger


# ------------------------------------------------
# model support
# ------------------------------------------------
from ..model.model import *


log = logger(__name__)

# =========================================================
# Mappers Support
# =========================================================


def BASIC_ID(x):
    if isinstance(x, str):
        return x.split(":")[-1]
    return x


def VALID(x):
    try:
        if isnan(x):
            return False
    except Exception:
        pass
    return True


ANNOTATION_FACTORY = {
    "List": list,
    "Dict": dict,
}


class Mapper:
    PYDANTIC = None
    _MAPPING = {}
    _REVERSE = {}

    @classmethod
    def _populate(cls):
        MAP = cls._MAPPING.get(cls)
        if MAP is None:
            MAP = cls._MAPPING[cls] = {}
            REVERSE = cls._REVERSE[cls] = {}
            # explore subclasses
            klasses = cls.mro()[:-1]
            for klass in reversed(klasses):
                for key in dir(klass):
                    value = getattr(klass, key)
                    if isinstance(value, tuple):
                        l = len(value)
                        if l == 2:
                            # is an attribute
                            MAP[key] = *value, None
                        elif l == 3:
                            MAP[key] = value

                        t_name = value[0]
                        if isinstance(t_name, str):
                            REVERSE[key] = t_name
                        elif t_name in (I,):
                            # inverse function of I -> I
                            REVERSE[key] = key
                        else:
                            log.warning("inverse of t_name: %s is unknown", t_name)

        return MAP

    @classmethod
    def _schemes(cls):
        base = {
            "id": "https://portal.ccoc-mlg.spec-cibernos.com/api/schema/{{ normalized.kind }}/latest",
            "ref": "aemet.observation",
            "type": "object",
            "ccoc-label": {"default": "Observación Estación Metereológica AEMET"},
            "properties": {
                "id": {"type": "string", "ccoc-label": {"default": "Id"}},
                "type": {
                    "type": "string",
                    "ccoc-label": {"default": "Type"},
                },
                # extra properties comes here
            },
            "ccoc-extraInformation": {
                "ccoc-defaultDisplayedAttributes": [],
                "ccoc-defaultMapMarkerIcon": {
                    "iconUrl": "",
                    "legendLabel": "",
                },
            },
        }

        MAP = cls._MAPPING.get(cls)
        if MAP is None:
            pass

    @classmethod
    def transform(cls, org: Dict, only_defined=False, **kw):
        assert isinstance(org, dict)
        result = {} if only_defined else dict(org)
        MAP = cls._populate()

        def parse(value, t_value, t_default):
            if VALID(value):
                if inspect.isfunction(t_value):
                    value = t_value(value)
                # is a fstring?
                elif isinstance(t_value, str):
                    value = t_value.format_map(org)
                # is a typing anotation?
                elif isinstance(t_value, _GenericAlias):
                    if t_value._name in ANNOTATION_FACTORY:
                        # example
                        # data = (r"Data", List[StatisticData], )
                        new_value = {
                            klass: [parse(v, klass, t_default) for v in value]
                            for klass in t_value.__args__
                        }
                        # create the value from Generic specification
                        factory = ANNOTATION_FACTORY[t_value._name]
                        value = factory(
                            itertools.zip_longest(
                                new_value.values(),
                                fillvalue=None,
                            )
                        )
                        value = value[0][0]  # TODO: review
                    else:
                        raise f"don't know how to deal with `{t_value}` typing yet!"
                elif inspect.isclass(t_value) and issubclass(t_value, Mapper):
                    # is another mapper?
                    value = t_value.pydantic(value)
                else:
                    value = t_value(value)
            else:
                value = t_default
            return value

        try:
            for key, (t_name, t_value, t_default) in MAP.items():
                # try to use a glom specification
                if isinstance(t_name, (str, list)):
                    try:
                        value = glom(org, t_name)
                        value = parse(value, t_value, t_default)
                        result[key] = value
                        continue
                    except Exception as why:
                        pass
                elif isinstance(t_name, tuple):
                    values = [org[k] for k in t_name]
                    value = t_value(*values)
                    result[key] = value
                    continue
                # try to use a direct regexp match or a function to get the name
                name = None
                if isinstance(t_name, str):
                    for k, v in org.items():
                        if m := re.match(t_name, k):
                            # name = m.group(0)
                            name = k  # take the key not the match
                            break
                else:
                    name = t_name(key)

                # if name:  # name in org
                value = org.get(name, t_default)
                value = parse(value, t_value, t_default)
                result[key] = value

        except Exception as why:  # pragma: nocover
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))
            log.error(f"key: {key} : value: {value}")

        return result

    @classmethod
    def item(cls, org, **extra):
        """Create a pydantic object as well. `source` is already transformed"""
        klass = getattr(cls, "PYDANTIC", None)
        if klass:
            if klass != IgnoreMapper:
                org.update(extra)
                try:
                    item = klass(**org)
                except ValidationError as why:
                    log.warning(
                        "FAILED Pydatic Validation: klass: [%s] : [%s]",
                        klass,
                        org,
                    )
                    log.warning(f"{why}")
                    item = None
                return item

        else:
            log.warning("[%s] has not defined a PYDANTIC class", cls)

    @classmethod
    def pydantic(cls, org, **extra):
        """Create a pydantic object as well. `source` is not yet transformed"""
        return cls.item(cls.transform(org, **extra), **extra)


class IgnoreMapper(Mapper):
    """A specific mapper to indicate we don't want to
    create any pydantic class explicity
    (it not forgotten or a mistake)
    """
