import aiohttp

from syncmodels.definitions import (
    DURI,
)

from . import iSession


class HTTPSession(iSession):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._session = None

    def __enter__(self, *args, **kw):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _create_connection(self, uri: DURI, **_uri):
        # uri = parse_uri(url, **kw)
        url = self._get_base_url()
        return aiohttp.ClientSession(base_url=url)


# iSession.SESSION_FACTORY[r"(http|https)://"] = HTTPSession
HTTPSession.register_itself(r"(http|https)://")


class TextLinesSession(HTTPSession):
    "An example of session with authentication with an external service"

    async def _process_response(self, response):
        stream, meta = await super()._process_response(response)
        _stream = []
        for data in stream:
            for line in data["result"].splitlines():
                item = {"result": line}
                _stream.append(item)
        return _stream, meta
