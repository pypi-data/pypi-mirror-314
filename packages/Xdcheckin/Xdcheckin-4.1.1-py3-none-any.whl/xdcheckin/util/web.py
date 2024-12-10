__all__ = ("compress_middleware", )

from aiohttp.hdrs import CACHE_CONTROL as _CACHE_CONTROL
from aiohttp.web import (
	middleware as _middleware, StaticResource as _StaticResource
)
from aiohttp_compress import compress_middleware as _compress_middleware

@_middleware
async def compress_middleware(req, handler):
	if isinstance(req.match_info.route.resource, _StaticResource):
		res = await _compress_middleware(req, handler)
		res.headers[_CACHE_CONTROL] = "public, max-age=86400"
		return res
	return await handler(req)
