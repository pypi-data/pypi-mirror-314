# -*- coding: UTF-8 -*-

import typing

import orjson
from starlette.responses import Response, StreamingResponse


class ORJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(
            content, option=orjson.OPT_STRICT_INTEGER)


class StreamResponse(StreamingResponse):
    pass
