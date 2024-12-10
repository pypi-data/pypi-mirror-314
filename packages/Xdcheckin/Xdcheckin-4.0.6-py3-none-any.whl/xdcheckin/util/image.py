__all__ = ("url_get_img", "b64_get_img", "video_get_img", "img_scan")

from asyncio.subprocess import (
	create_subprocess_exec as _create_subprocess_exec,
	PIPE as _PIPE
)
from base64 import b64decode
from io import BytesIO as _BytesIO
from aiohttp import request as _request, ClientTimeout as _ClientTimeout
from PIL.Image import open as _open, Image as _Image
from xdcheckin.util.network import user_agent_base as _user_agent_base

_requests_headers = {"User-Agent": _user_agent_base}
_requests_timeout = _ClientTimeout(300)

def _img_open(data: bytes):
	return _open(_BytesIO(data))

async def url_get_img(url: str, ses = None):
	"""Fetch image from a given URL.

	:param url: URL.
	:param ses: An ``aiohttp.ClientSession`` instance. Optional.
	"""
	data = None
	if ses:
		res = await ses.get(
			url, headers = _requests_headers,
			timeout = _requests_timeout
		)
		if res.status == 200:
			data = await res.read()
	else:
		async with _request(
			"GET", url, headers = _requests_headers
		) as res:
			if res.status == 200:
				data = await res.read()
	return _img_open(data) if data else None

async def b64_get_img(b64: str):
	"""Fetch image from a given base 64 string.

	:param url: Base 64 string.
	:param ses: An ``aiohttp.ClientSession`` instance. Optional.
	"""
	return _img_open(b64decode(b64))

async def _video_m3u8_get_ts_url(url: str, ses = None, len_limit = 256):
	if ses:
		res = await ses.get(url, headers = {})
		assert res.status == 200 and res.content_length < len_limit
		text = await res.text()
	else:
		async with _request(
			"GET", url, headers = _requests_headers
		) as res:
			assert (
				res.status == 200 and
				res.content_length < len_limit
			)
			text = await res.text()
	ts = text.split()[-1]
	assert ts.endswith(".ts")
	return ts

try:
	from xdcheckin_ffmpeg import ffmpeg as _get_ffmpeg
	_ffmpeg = _get_ffmpeg()
	async def video_get_img(url: str, ses = None, len_limit: int = 256):
		"""Extract a frame from video stream.
		Requires ``xdcheckin[image]``.

		:param url: URL of the stream.
		:param ses: An ``aiohttp.ClientSession`` instance. Optional.
  		:param len_limit: Length limit of the M3U8 data.
		Default is ``256``.
		:return: Frame in ``PIL.Image.Image`` on success.
		"""
		if url.startswith("rtsp://"):
			proc = await _create_subprocess_exec(
				_ffmpeg, "-v", "quiet", "-flags", "low_delay",
				"-fflags", "discardcorrupt+flush_packets",
				"-probesize", "2048",
				"-rtsp_transport", "tcp", "-i", url,
				"-an", "-pix_fmt", "yuvj420p", "-vframes", "1",
				"-f", "image2", "-g", "1", "-", stdout = _PIPE
			)
		else:
			if url.endswith(".m3u8"):
				ts = await _video_m3u8_get_ts_url(
					url = url, ses = ses,
					len_limit = len_limit
				)
				url = f"{url[: url.rfind('/')]}/{ts}"
			proc = await _create_subprocess_exec(
				_ffmpeg, "-v", "quiet", "-flags", "low_delay",
				"-fflags", "discardcorrupt+flush_packets",
				"-probesize", "2048", "-i", url,
				"-an", "-pix_fmt", "yuvj420p", "-vframes", "1",
				"-f", "image2", "-g", "1", "-", stdout = _PIPE
			)
		return _img_open((await proc.communicate())[0])
except ImportError:
	async def video_get_img(url: str, ses = None, len_limit: int = 384):
		"""Dummy fallback for ``video_get_img()``.

		:param url: URL of the stream.
		:param ses: An ``aiohttp.ClientSession`` instance. Optional.
  		:param len_limit: Length limit of the M3U8 data.
		Default is ``256``.
		:return: Dummy ``PIL.Image.Image``.
		"""
		img = _Image()
		img.info["msg"] = "Please install ``xdcheckin[image]``."
		return img

try:
	from pyzbar.pyzbar import decode as _decode, ZBarSymbol as _ZBarSymbol
	def img_scan(img):
		"""Scan and decode qrcodes in an Image.
		Requires ``xdcheckin[image]``.

		:param img: ``PIL.Image.Image`` Image.
		:return: Decoded strings.
		"""
		assert img.height and img.width
		return [s.data.decode("utf-8") for s in _decode(
			img, (_ZBarSymbol.QRCODE, )
		)]
except ImportError:
	def img_scan(img):
		"""Dummy fallback for ``img_scan()``.

		:param img: ``PIL.Image.Image`` Image.
		:return: ``[]``.
		"""
		return []
