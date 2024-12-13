import asyncio
import tarfile
import zipfile
import io
import json
import os
import gzip
import bz2
import lzma as xz

import pandas as pd

from agptools.helpers import build_uri, parse_xuri, parse_uri
from agptools.logs import logger
from agptools.files import ContentIterator

from syncmodels.definitions import (
    BODY_KEY,
    KIND_KEY,
    METHOD_KEY,
    MONOTONIC_KEY,
    # MONOTONIC_SINCE,
    MONOTONIC_SINCE_KEY,
    MONOTONIC_SINCE_VALUE,
    URI,
    DURI,
    WAVE_LAST_KEY,
    WAVE_RESUMING_INFO_KEY,
)
from syncmodels.mapper.mapper import Mapper
from syncmodels.auth import iAuthenticator

from syncmodels.http import (
    guess_content_type,
    APPLICATION_JSON,
    APPLICATION_ZIP,
    APPLICATION_GTAR,
    APPLICATION_MS_EXCEL,
    APPLICATION_OCTET_STREAM,
)

from syncmodels.crawler import iRunner

from ..crud import parse_duri, DEFAULT_DATABASE, DEFAULT_NAMESPACE, tf

from ..context import iContext
from ..schema import iSchema, StructShema
from ..registry import iRegistry
from ..requests import iResponse

log = logger(__name__)


class iSession(iContext, iSchema, iRegistry):  # , iAuthenticator):
    "The base for all 3rd party session accessors"

    DEFAULT_METHOD = "get"

    RESPONSE_META = ["headers", "links", "real_url"]

    CACHE = {}
    "some data to be cached and shared"

    QUERY_BODY_KEY = "json"
    PARAMS_KEY = "params"

    def __init__(self, bot, **kw):
        self.bot = bot
        self.connection_pool = {}
        self.headers = {}
        self.context = kw

    async def _schema(self, uri: URI, data=None, **kw):
        schema = self.CACHE.get(uri) # .get(_uri[KIND_KEY])
        if not schema:
            schema = await self._get_schema(uri, data, **kw)
        return schema

    async def _create_connection(self, uri: DURI, **_uri):
        raise NotImplementedError()

    def _get_base_url(self, **kw) -> URI:
        url = build_uri(
            fscheme=self.context["fscheme"],
            xhost=self.context["xhost"],
            **kw,
        )
        return url

    async def _process_response(self, response):
        def expand(value):
            iterator = getattr(value, "items", None)
            if iterator:
                value = {k: expand(v) for k, v in iterator()}
            return value

        meta = {
            # k: expand(getattr(response, k, None))
            # for k in self.RESPONSE_META
            # if hasattr(response, k)
        }
        headers = getattr(response, "headers", {})
        meta.update(headers)
        content_type = guess_content_type(headers)

        try:
            if content_type == APPLICATION_JSON:
                stream = await response.json()

            elif content_type in (
                APPLICATION_ZIP,
                APPLICATION_GTAR,
            ):
                raw = await response.read()  # bytes object
                # stream = []
                # for thing in ContentIterator(name='', raw=raw):
                #     stream.extend(thing)
                stream = [thing for thing in ContentIterator(name="", raw=raw)]
            elif content_type in (APPLICATION_MS_EXCEL,):
                raw = await response.read()  # bytes object
                df = pd.read_excel(io.BytesIO(raw))
                stream = json.loads(df.to_json(orient="records"))
            elif content_type in (APPLICATION_OCTET_STREAM,):
                raw = await response.read()  # bytes object
                try:
                    df = pd.read_csv(
                        io.StringIO(raw.decode("ISO-8859-1")),
                        sep=None,
                        engine="python",
                        decimal=",",
                    )
                    stream = json.loads(df.to_json(orient="records"))
                except Exception as why:
                    log.error("Error processing CSV [%s]", why)
                    log.error("content_type: %s", content_type)
                    log.error("response    : %s", response)
                    raise
            else:
                stream = await response.text()
                assert isinstance(stream, str)
                # stream = [{'data': block} for block in stream.splitlines()]
                stream = [{"result": stream}]

        except Exception as why:
            log.error("why: [%s]", why)

            log.error("content_type : %s", content_type)
            log.error("response     : %s", response)
            # log.error("response.text: %s", response)

            raise

        return stream, meta

    def _get_connection_key(self, uri: DURI):
        namespace = tf(uri.get("fscheme", DEFAULT_NAMESPACE))
        database = tf(uri.get("host", DEFAULT_DATABASE))
        key = namespace, database
        return key

    async def _get_connection(self, uri: DURI, **kw):
        key = self._get_connection_key(uri)
        connection = self.connection_pool.get(key) or await self._create_connection(uri)
        return connection

    @classmethod
    async def new(cls, url, bot, **context):
        def score(item):
            "score by counting how many uri values are not None"
            options, m = item
            _uri = parse_xuri(url)
            sc = 100 * len(m.groups()) + len(
                [_ for _ in _uri.values() if _ is not None]
            )
            return sc, options

        blue, factory, args, kw = cls.get_factory(url, __klass__=cls, score=score)
        if factory:
            uri = parse_uri(url, **context)
            try:
                context.update(kw)
                item = factory(bot=bot, *args, **uri)
                return item
            except Exception as why:  # pragma: nocover
                print(why)
                foo = 1

        # option = cls.locate(url, __klass__=cls, score=score)
        # if option:
        #     uri = parse_uri(url)
        #     factory, info = option
        #     for __key__, (args, kw) in info.items():
        #         try:
        #             context.update(kw)
        #             item = factory(bot=bot, *args, **uri, **context)
        #             return item
        #         except Exception as why:
        #             print(why)

        raise RuntimeError(f"Unable to create a {cls} for url: {url}")

    async def get(self, url, headers=None, params=None, **kw) -> iResponse:
        "Note: Returns is not properly a iResponse, but we mimic the same interface"
        headers = headers or {}
        params = params or {}
        connection = await self._get_connection(url, **headers, **params, **kw)
        return await connection.get(url, headers=headers, params=params, **kw)

    async def _get_schema(self, uri: URI, data=None, **kw):
        # uri = _uri["uri"]
        # kind = _uri[KIND_KEY]
        # schema = self.CACHE.setdefault(uri, {})[kind] = await self._inspect_schema(_uri, data)
        schema = self.CACHE.get(uri)
        if not schema:
            schema = await self._inspect_schema(uri, data, **kw)
            if schema.monotonic_since_key:
                self.CACHE[uri] = schema

        return schema

    async def _inspect_schema(self, uri
: URI, data=None, **kw) -> StructShema:
        """performs an introspection to figure-out the schema
        for a particular kind object
        """
        schema = StructShema(
            names=[],
            types=[],
            d_fields={},
            monotonic_since_key="",
            struct={},
        )
        return schema

    async def update_params(self, url, params, context):
        """
        Last chance to modify params based on context for a specific iSession type

        context
        {'crawler__': <SQLiteCrawler>:dummy,
         'bot__': <HTTPBot>:httpbot-0,
         'wave_info__': [],
         'kind__': 'mysensor_stream',
         'func__': 'get_data',
         'meta__': {'foo': 'bar'},
         'prefix__': <Template memory:7c699f532200>,
         'prefix_uri__': 'test://test/mysensor_stream:TubeSnap:mysensor_stream_AINB50945878432336',
         'url__': 'sqlite:///tmp/kraken1727939402.3510203.592664656/db.sqlite',
         'wave_last__': [{'wave': {'id': 'TubeWave:6fwb9uiw3obw0dsijxm4',
                                   'kind__': 'mysensor_stream',
                                   'params__': {},
                                   'prefix_uri__': 'test://test/{{ kind__ }}:{{ id }}',
                                   'wave__': 1727939442812620427},
                          'items': [{'datetime': '2025-03-13T09:10:17Z',
                                     'id': 'TubeSnap:mysensor_stream_AINB50945878432336',
                                     'id__': 'test://test/mysensor_stream:AINB50945878432336',
                                     'value': 25.0,
                                     'wave__': 1727939442812620427}]}],
         'params__': {}}

         # we expect
         call_kw
         {'url': 'sqlite://test/tmp/kraken1727980024.3481097.245022830/db.sqlite',
          'headers': {},
          'params': {'since_key__': 'datetime', 'since_value__': '2025-03-27T20:27:07Z'}}


        """
        # try to convert from WAVE_LAST_KEY -> params that EndPoint
        # will understand

        # 1. get the schema that maps attributes
        # _uri = parse_uri(url, **context)
        # schema = await self._schema(url, **context)
        # monotonic_since_key = schema.monotonic_since_key

        # 2. iterate over waves info
        # TODO: agp: REVIEW if is necessary to do anything here
        # kind = context[KIND_KEY]
        # MAPPER = self.bot.parent.MAPPERS[kind]
        # MAPPER._populate()
        # REVERSE = Mapper._REVERSE.get(kind, {})

        for wave0 in context.get(WAVE_LAST_KEY, []):

            # 3. search these values in the items that belongs to the
            # last wave (from last insertion in the tube)
            for item in wave0.get("items", []):
                # if monotonic_since_key in item:
                #     params[MONOTONIC_SINCE_KEY] = monotonic_since_key
                #     params[MONOTONIC_SINCE_VALUE] = item[monotonic_since_key]
                #     break
                if resuming_info := item.get(WAVE_RESUMING_INFO_KEY):
                    assert (
                        len(resuming_info) == 1
                    ), "multiples resuming keys are not alloewd (review storage.put())"
                    key, value = resuming_info.popitem()
                    params[MONOTONIC_SINCE_KEY] = key
                    params[MONOTONIC_SINCE_VALUE] = value
                    break
            # else:
            #     schema = await self._schema(url, **context)
            #     monotonic_since_key = schema.monotonic_since_key
            #     log.warning(
            #         "MONOTONIC_SINCE_KEY [%s] is missing in wave: %s: schema=[%s]",
            #         monotonic_since_key,
            #         wave0,
            #         schema.__dict__,
            #     )
            #     continue
            break

        call_kw = {
            "url": url,
            "headers": self.headers,
        }
        if context.get(METHOD_KEY, "get").lower() in ("post", "put"):
            if body := context.get(BODY_KEY):
                call_kw[self.QUERY_BODY_KEY] = body
        else:
            call_kw[self.PARAMS_KEY] = params
        return call_kw


class iActiveSession(iSession, iRunner):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.running = False

    async def start(self):
        pass

    async def stop(self):
        pass

    async def run(self):
        while self.running:
            await asyncio.sleep(1)


if __name__ == "__main__":
    import pickle

    data = pickle.load(open("/tmp/xml.pickle", "rb"))

    stream = []
    for thing in ContentIterator(**data):
        stream.append(thing)
