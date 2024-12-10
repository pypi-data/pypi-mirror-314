# -*- coding: utf-8 -*-

__all__ = (
	"server_routes", "server_config_key", "create_server", "start_server"
)

from asyncio import create_task as _create_task, sleep as _sleep, run as _run
from json import dumps as _dumps, loads as _loads
from os.path import basename as _basename
from pathlib import Path as _Path
from sys import argv as _argv, exit as _exit, stderr as _stderr
from threading import (
	current_thread as _current_thread, main_thread as _main_thread
)
from time import time as _time
from uuid import uuid4 as _uuid4
from aiohttp import request as _request
from aiohttp.web import (
	AppKey as _AppKey, Application as _Application, Response as _Response,
	RouteTableDef as _RouteTableDef, run_app as _run_app
)
from aiohttp_session import get_session as _get_session, setup as _setup
from aiohttp_session import SimpleCookieStorage as _SimpleCookieStorage
from xdcheckin.core.chaoxing import Chaoxing as _Chaoxing
from xdcheckin.core.locations import locations as _locations
from xdcheckin.core.xidian import (
	IDSSession as _IDSSession, Newesxidian as _Newesxidian
)
from xdcheckin.util.image import (
	video_get_img as _video_get_img, img_scan as _img_scan
)
from xdcheckin.util.network import is_valid_host as _is_valid_host
from xdcheckin.util.types import TimestampDict as _TimestampDict
from xdcheckin.util.version import (
	compare_versions as _compare_versions, version as _version
)
from xdcheckin.util.web import compress_middleware as _compress_middleware

server_routes = _RouteTableDef()
server_config_key = _AppKey("config", dict)

_static_dir_path = _Path(__file__).parent.resolve()
server_routes.static("/static", _static_dir_path.joinpath("static"))

_index_html_str = _static_dir_path.joinpath(
	"templates", "index.html"
).read_text(encoding = "utf-8")
@server_routes.get("/")
async def _index_html(req):
	return _Response(
		text = _index_html_str, content_type = "text/html"
	)

@server_routes.post("/xdcheckin/get_version")
async def _xdcheckin_get_version(req):
	return _Response(text = _version)

_xdcheckin_get_update_time = 0
_xdcheckin_get_update_data = ""
@server_routes.post("/xdcheckin/get_update")
async def _xdcheckin_get_update(req):
	global _xdcheckin_get_update_time, _xdcheckin_get_update_data
	update, time = False, _time()
	if 1 or time < _xdcheckin_get_update_time + 3600:
		_xdcheckin_get_update_time = time
		try:
			async with _request(
				"GET",
				"https://api.github.com/repos/Pairman/Xdcheckin/releases/latest"
			) as res:
				assert res.status == 200
				data = await res.json()
			update = _compare_versions(
				_version, data["tag_name"]
			) == 1
		except Exception:
			update = False
		_xdcheckin_get_update_data = _dumps({
			"tag_name": data["tag_name"],
			"name": data["name"],
			"author": data["author"]["login"],
			"body": data["body"].replace("\r\n", "<br>"),
			"published_at": data["published_at"],
			"html_url": data["html_url"],
			"assets": [{
				"name": asset["name"],
				"size": asset["size"],
				"browser_download_url":
				asset["browser_download_url"]
			} for asset in data["assets"]],
			"updatable": True
		}) if update else _dumps({"updatable": False})
	return _Response(
		text = _xdcheckin_get_update_data,
		content_type = "application/json",
		status = 200 if _xdcheckin_get_update_data else 500
	)

@server_routes.post("/ids/login")
async def _ids_login(req):
	try:
		data = await req.json()
		username, password = data["username"], data["password"]
		assert username and password, "Missing username or password."
		async with _IDSSession(
			service = "https://learning.xidian.edu.cn/cassso/xidian"
		) as ids:
			assert await ids.login_prepare(), "IDS login failed."
			captcha = False
			for _ in range(6):
				captcha = await ids.captcha_handle_captcha()
				if captcha:
					break
			assert captcha, "CAPTCHA verification failed."
			ret = await ids.login_username_finish(account = {
				"username": username, "password": password
			})
		assert ret["logged_in"], "IDS login failed."
		cookies = ret["cookies"].filter_cookies("https://chaoxing.com")
		_data = {
			"username": "", "password": "", "cookies":
			_dumps({k: v.value for k, v in cookies.items()}),
			"chaoxing_config": data.get("chaoxing_config", "{}")
		}
		return await _chaoxing_login(req = req, data = _data)
	except Exception as e:
		return _Response(
			text = _dumps({"err": f"{e}"}),
			content_type = "application/json"
		)

@server_routes.post("/chaoxing/login")
async def _chaoxing_login(req, data = None):
	try:
		ses = await _get_session(req)
		server_ses = req.app[server_config_key]["sessions"].setdefault(
			ses.setdefault("uuid", f"{_uuid4()}"), {}
		)
		if not data:
			data = await req.json()
		username, password, cookies = (
			data["username"], data["password"], data["cookies"]
		)
		assert (
			(username and password) or cookies
		), "Missing username, password or cookies."
		config = {
			"chaoxing_course_get_activities_courses_limit": 36,
			"chaoxing_checkin_location_address_override_maxlen": 13,
			**_loads(data["chaoxing_config"])
		}
		cx = server_ses.pop("cx", None)
		if cx:
			_create_task(cx.__aexit__(None, None, None))
		nx = server_ses.pop("nx", None)
		if nx:
			_create_task(nx.__aexit__(None, None, None))
		server_ses["cx"] = cx = await _Chaoxing(
			username = username, password = password,
			cookies = _loads(cookies) if cookies else None,
			config = config
		).__aenter__()
		assert cx.logged_in, "Chaoxing login failed."
		if cx.fid == "16820":
			server_ses["nx"] = nx = _Newesxidian(chaoxing = cx)
			await nx.__aenter__()
			_create_task(nx.curriculum_get_curriculum())
		data = {
			"fid": cx.fid, "courses": cx.courses, "cookies":
			_dumps({k: v.value for k, v in cx.cookies.items()})
		}
	except Exception as e:
		if server_ses.get("cx"):
			_create_task(server_ses["cx"].__aexit__(
				None, None, None
			))
		if server_ses.get("nx"):
			_create_task(server_ses["nx"].__aexit__(
				None, None, None
			))
		data = {"err": f"{e}"}
	finally:
		return _Response(
			text = _dumps(data), content_type = "application/json"
		)

@server_routes.post("/newesxidian/extract_url")
async def _newesxidian_extract_url(req):
	try:
		data = await req.json()
		ses = await _get_session(req)
		nx = req.app[server_config_key]["sessions"][ses["uuid"]]["nx"]
		assert nx.logged_in
		livestream = await nx.livestream_get_live_url(
			livestream = {"live_id": f"{data}"}
		)
		return _Response(text = livestream["url"])
	except Exception as e:
		return _Response(text = f"{e}")

@server_routes.post("/chaoxing/get_curriculum")
async def _chaoxing_get_curriculum(req):
	try:
		with_live = await req.json()
		ses = await _get_session(req)
		xx = req.app[server_config_key]["sessions"][ses["uuid"]][
			"nx" if with_live else "cx"
		]
		assert xx.logged_in
		data = await xx.curriculum_get_curriculum()
	except Exception:
		data = {}
	finally:
		return _Response(
			text = _dumps(data), content_type = "application/json"
		)

@server_routes.post("/chaoxing/get_activities")
async def _chaoxing_get_activities(req):
	try:
		ses = await _get_session(req)
		cx = req.app[server_config_key]["sessions"][ses["uuid"]]["cx"]
		assert cx.logged_in
		data = await cx.course_get_activities()
		status = 200
	except Exception:
		data = {}
		status = 500
	finally:
		return _Response(
			text = _dumps(data), status = status,
			content_type = "application/json"
		)			

@server_routes.post("/chaoxing/checkin_checkin_location")
async def _chaoxing_checkin_checkin_location(req):
	try:
		data = await req.json()
		assert data["activity"]["active_id"], "No activity ID given."
		ses = await _get_session(req)
		cx = req.app[server_config_key]["sessions"][ses["uuid"]]["cx"]
		assert cx.logged_in, "Not logged in."
		data["activity"]["active_id"] = f"""{
			data['activity']['active_id']
		}"""
		result = await cx.checkin_checkin_location(
			activity = data["activity"], location = data["location"]
		)
		data = result[1]
	except Exception as e:
		data = {"msg": f"Checkin error. ({e})", "params": {}}
	finally:
		return _Response(
			text = _dumps(data), content_type = "application/json"
		)

@server_routes.post("/chaoxing/checkin_checkin_qrcode_url")
async def _chaoxing_checkin_checkin_qrcode_url(req):
	try:
		data = await req.json()
		ses = await _get_session(req)
		cx = req.app[server_config_key]["sessions"][ses["uuid"]]["cx"]
		assert cx.logged_in, "Not logged in."
		vsrc = data.get("video")
		if vsrc:
			with await _video_get_img(
				url = vsrc, ses = cx
			) as img:
				assert (
					img.height and img.width
				), f"Zero-sized image. ({img.info.get('msg')})"
				urls = _img_scan(img)
			assert urls, "No Qrcode detected."
			qr_urls = [s for s in urls if "widget/sign/e" in s]
			assert qr_urls, f"No checkin URL in {urls}."
			data["url"] = next(iter(qr_urls))
		result = await cx.checkin_checkin_qrcode_url(
			url = data["url"], location = data["location"]
		)
		data = result[1]
	except Exception as e:
		data = {"msg": f"Checkin error. ({e})", "params": {}}
	finally:
		return _Response(
			text = _dumps(data), content_type = "application/json"
		)

async def _vacuum_server_sessions_handler(ses):
	for key in {"nx", "cx"}:
		if key in ses:
			await ses[key].__aexit__(None, None, None)

async def _vacuum_server_sessions(app):
	sessions = app[server_config_key]["sessions"]
	t = (
		app[server_config_key]["sessions_vacuum_days"] * 86400
		- 18000 - _time() % 86400
	)
	if t <= 0:
		return
	while True:
		await _sleep(t)
		_create_task(sessions.vacuum(
			seconds = t, handler = _vacuum_server_sessions_handler
		))

def create_server(config: dict = {}):
	"""Create a Xdcheckin server.

	:param config: Configurations.
	:return: Xdcheckin server.
	"""
	if not isinstance(config, dict):
		raise TypeError(
			f"config type must be dict, "
			f"not {type(config).__name__}."
		)
	app = _Application()
	app.middlewares.append(_compress_middleware)
	app.add_routes(server_routes)
	app[server_config_key] = {
		"sessions": {}, "sessions_vacuum_days": 1, **config
	}
	_setup(app, _SimpleCookieStorage(
		cookie_name = "xdcheckin", max_age = 604800
	))
	return app

def start_server(
	host: str = "0.0.0.0", port: int = 5001, config: dict = {}, loop = None
):
	"""Run a Xdcheckin server.

	:param host: IP address.
	:param port: Port.
	:param config: Configurations.
	:param loop: Event loop. Only necessary in non-main thread.
	"""
	app = create_server(config = {"sessions": _TimestampDict(), **config})
	async def _startup(app):
		app[server_config_key]["_vacuum_task"] = _create_task(
			_vacuum_server_sessions(app = app)
		)
		h = f"{f'[{host}]' if _is_valid_host(host) == 6 else host}"
		print(f"Starting Xdcheckin server on {h}:{port}.")
	async def _shutdown(app):
		await app[server_config_key]["sessions"].vacuum(
			handler = _vacuum_server_sessions_handler
		)
	app.on_startup.append(_startup)
	app.on_shutdown.append(_shutdown)
	try:
		_run_app(
			app, host = host, port = port, loop = loop,
			handle_signals = _current_thread() == _main_thread(),
			handler_cancellation = True, print =
			lambda _: print("Server started. Press Ctrl+C to quit.")
		)
	except KeyboardInterrupt:
		pass
	finally:
		_run(app.shutdown())
		_run(app.cleanup())
		print("Server shut down.")

def _main():
	host, port = "0.0.0.0", 5001
	bn = _basename(_argv[0])
	help = (
		f"{bn} - Xdcheckin Server Commandline Tool "
		f"{_version}\n\n"
		f"Usage: \n"
		f"  {bn} [<host> <port>]\t"
		"Start server on the given host and port.\n"
		f"  {' ' * len(bn)}\t\t\tDefault is '{host}:{port}'.\n"
		f"  {bn} -h|--help\t\tShow help."
	)
	if len(_argv) == 2 and _argv[1] in ("-h", "--help"):
		print(help)
		_exit()
	elif not len(_argv) in (1, 3):
		print(help, file = _stderr)
		_exit(2)
	if len(_argv) == 3:
		host = _argv[1]
		if not _is_valid_host(host):
			print(f"Invalid host '{_argv[1]}'", file = _stderr)
			_exit(2)
		port = int(_argv[2]) if _argv[2].isdigit() else 0
		if not 0 < port < 65536:
			print(f"Invalid port '{_argv[2]}'", file = _stderr)
			_exit(2)
	start_server(host = host, port = port)
