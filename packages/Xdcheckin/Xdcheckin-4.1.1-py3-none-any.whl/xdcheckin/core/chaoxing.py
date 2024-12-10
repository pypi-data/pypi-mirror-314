# -*- coding: utf-8 -*-

__all__ = ("Chaoxing", )

from asyncio import (
	create_task as _create_task, gather as _gather, Semaphore as _Semaphore
)
from copy import deepcopy as _deepcopy
from json import loads as _loads, dumps as _dumps
from math import trunc as _trunc
from random import shuffle as _shuffle, uniform as _uniform
from re import compile as _compile, DOTALL as _DOTALL
from time import time as _time 
from aiohttp import ClientTimeout as _ClientTimeout
from Crypto.Cipher.AES import MODE_ECB as _MODE_ECB
from yarl import URL as _URL
from xdcheckin.util.captcha import (
	chaoxing_captcha_get_checksum as _chaoxing_captcha_get_checksum,
	solve_captcha_rotate as _solve_captcha_rotate,
	solve_captcha_slide as _solve_captcha_slide
)
from xdcheckin.util.encryption import (
	encrypt_aes as _encrypt_aes,
	chaoxing_get_identifier as _chaoxing_get_identifier,
	chaoxing_get_devicecode as _chaoxing_get_devicecode,
	chaoxing_get_schild as _chaoxing_get_schild
)
from xdcheckin.util.image import url_get_img as _url_get_img
from xdcheckin.util.network import user_agent_base as _user_agent_base
from xdcheckin.util.session import CachedSession as _CachedSession
from xdcheckin.util.time import strftime as _strftime

_Chaoxing___init___regex1 = _compile(r"( \(@Kalimdor\)_.*?)?$")
_Chaoxing___init___regex2 = _compile(r" (\(schild:.*?\) )?\(device:")
_Chaoxing_captcha_get_captcha_regex1 = _compile(
	r"captchaId: '([0-9A-Za-z]{32})'"
)
_Chaoxing_captcha_get_captcha_regex2 = _compile(r"t\":(\d+)")
_Chaoxing_login_username_yz_regex = _compile(r"enc.*?([0-9a-f]{32})", _DOTALL)
_Chaoxing_course_get_courses_regex1 = _compile(
	r"course-cover.*?courseid=(\d+)&clazzid=(\d+).*?(?:(not-open).*?)?"
	r"course-name.*?>(.*?)<.*?class=\"line2.*?>(.*?)<.*?\n"
	r"(?:[^\n]*?(\d+-\d+-\d+)～(\d+-\d+-\d+))?", _DOTALL
)
_Chaoxing_course_get_courses_regex2 = _compile(r", |,|，|、")
_Chaoxing_checkin_get_location_error_regex = _compile(
	r"ifopenAddress\" value=\"(\d)\"(?:.*?locationText\" value=\"(.*?)\""
	r".*?locationLatitude\" value=\"(\d+\.\d+)\".*?locationLongitude\" "
	r"value=\"(\d+\.\d+)\".*?locationRange\" value=\"(\d+))?", _DOTALL
)
_Chaoxing_checkin_do_analysis_regex = _compile(r"([0-9a-f]{32})")
_Chaoxing_checkin_do_presign_regex = _compile(
	r"ifopenAddress\" value=\"(\d)\"(?:.*?locationText\" value=\"(.*?)\""
	r".*?locationLatitude\" value=\"(\d+\.\d+)\".*?locationLongitude\" "
	r"value=\"(\d+\.\d+)\".*?locationRange\" value=\"(\d+))?"
	r"|(zsign_success)", _DOTALL
)
_Chaoxing_checkin_do_sign_regex = _compile(r"validate_([0-9A-Fa-f]{32})")
_Chaoxing_checkin_checkin_qrcode_url_regex = _compile(
	r"id=(\d+).*?([0-9A-F]{32})"
)

_Chaoxing_config_base = {
	"requests_headers": {
		"User-Agent":
		f"{_user_agent_base} (device:MNA-LX9) Language/zh_CN com.chaoxi"
		"ng.mobile.xuezaixidian/ChaoXingStudy_1000149_6.3.7_android_pho"
		"ne_6005_249"
	},
	"requests_cache_enabled": True,
	"requests_timeout": 60,
	"chaoxing_device_identifier": "",
	"chaoxing_device_code": "",
	"chaoxing_course_get_activities_courses_limit": 32,
	"chaoxing_course_get_activities_workers": 16,
	"chaoxing_checkin_location_address_override_maxlen": 0,
	"chaoxing_checkin_location_randomness": True
}

class Chaoxing:
	"""Common Chaoxing APIs.
	"""
	__async_ctxmgr = __session = __secrets = None
	__config = __courses = __meeting_courses = {}
	__fid = __uid = "0"
	__name = ""
	__logged_in = False

	def __init__(
		self, username: str = "", password: str = "", cookies = {},
		config: dict = {}
	):
		"""Create a Chaoxing instance and login.

		:param username: Chaoxing username.
		Unused if ``cookies`` is given.
		:param password: Chaoxing password.
		Unused if ``cookies`` is given.
		:param cookies: Cookies from previous login.
		Overrides ``username`` and ``password`` if given.
		:param config: Configurations.
		"""
		if not self.__async_ctxmgr is None:
			return
		assert (username and password) or cookies
		assert isinstance(config, dict)
		self.__config = _deepcopy(_Chaoxing_config_base)
		self.__config.update(config)
		headers = self.__config["requests_headers"]
		ident = self.__config["chaoxing_device_identifier"]
		if ident:
			ua_parts = _Chaoxing___init___regex2.split(
				_Chaoxing___init___regex1.sub(
					f" (@Kalimdor)_{ident}",
					headers["User-Agent"], 1
				)
			)
			headers["User-Agent"] = f"""{ua_parts[0]} (schild:{
				_chaoxing_get_schild(f'(device:{ua_parts[2]}')
			}) (device:{ua_parts[2]}"""
		timeout = self.__config["requests_timeout"]
		self.__session = _CachedSession(
			headers = headers,
			timeout = _ClientTimeout(timeout) if timeout else None,
			cache_enabled = self.__config["requests_cache_enabled"]
		)
		self.__courses = {}
		self.__meeting_courses = {}
		self.__secrets = {
			"username": f"{username}", "password": f"{password}",
			"cookies": cookies
		}

	async def __aenter__(self):
		if not self.__async_ctxmgr is None:
			return self
		self.__async_ctxmgr = True
		await self.__session.__aenter__()
		username, password, cookies = self.__secrets.values()
		if cookies:
			self.__name, cookies, self.__logged_in = (
				await self.login_cookies(
					account = self.__secrets
				)
			).values()
		if not self.__logged_in and username and password:
			for f in (
				self.login_username_fanya,
				self.login_username_v3,
				self.login_username_v21,
				self.login_username_v25,
				self.login_username_v31,
				self.login_username_xxk,
				self.login_username_xxt,
				self.login_username_v2,
				self.login_username_v11,
				self.login_username_v24,
				self.login_username_2,
				self.login_username_mylogin1,
				self.login_username_yz
			):
				self.__name, cookies, self.__logged_in = (
					await f(account = self.__secrets)
				).values()
				if self.__logged_in:
					break
		if not self.logged_in:
			return self
		if "fid" in cookies:
			self.__fid = cookies["fid"].value
		self.__uid = cookies["_uid"].value
		self.__session.cookies = cookies 
		self.__secrets["device_code"] = self.__config[
			"chaoxing_device_code"
		] or _chaoxing_get_devicecode(self.__config[
			"chaoxing_device_identifier"
		] or _chaoxing_get_identifier(self.__uid))
		_meeting_courses = _create_task(
			self.course_get_meeting_courses()
		)
		self.__courses = await self.course_get_courses()
		self.__meeting_courses = {k: v for k, v in (
			await _meeting_courses
		).items() if not k in self.__courses}
		self.__secrets["courses"] = {
			**self.__courses, **self.__meeting_courses
		}
		return self

	async def __aexit__(self, *args, **kwargs):
		if not self.__async_ctxmgr:
			return
		await self.__session.__aexit__(*args, **kwargs)
		self.__secrets = None
		self.__fid = self.__uid = "0"
		self.__courses = {}
		self.__meeting_courses = {}
		self.__logged_in = False
		self.__async_ctxmgr = False

	@property
	def logged_in(self):
		return self.__logged_in

	@property
	def fid(self):
		return self.__fid

	@property
	def uid(self):
		return self.__uid

	@property
	def name(self):
		return self.__name

	@property
	def courses(self):
		return self.__secrets["courses"]

	@property
	def cookies(self):
		return self.__session.cookies

	async def get(self, *args, **kwargs):
		return await self.__session.get(*args, **kwargs)

	async def post(self, *args, **kwargs):
		return await self.__session.post(*args, **kwargs)

	async def captcha_get_captcha(self, captcha: dict = {"type": "rotate"}):
		"""Get CAPTCHA.

		:param type: CAPTCHA type. Supported: "rotate" and "slide".
		:return: CAPTCHA ID, images and token.
		"""
		if not "captcha_id" in self.__secrets:
			url1 = "https://mobilelearn.chaoxing.com/front/mobile/sign/js/mySignCaptchaUtils.js"
			res1 = await self.__session.get(url1, ttl = 2592000)
			match = _Chaoxing_captcha_get_captcha_regex1.search(
				await res1.text()
			)
			self.__secrets["captcha_id"] = match[1] if match else ""
		captcha_id = self.__secrets["captcha_id"]
		url2 = "https://captcha.chaoxing.com/captcha/get/conf"
		params2 = {
			"callback": "cx_captcha_function",
			"captchaId": captcha_id, "_": _trunc(_time() * 1000)
		}
		res2 = await self.__session.get(url2, params = params2)
		captcha = {
			**captcha, "captcha_id": captcha_id, "server_time":
			_Chaoxing_captcha_get_captcha_regex2.search(
				await res2.text()
			)[1]
		}
		captcha_key, token, iv = _chaoxing_captcha_get_checksum(
			captcha = captcha
		)
		url3 = "https://captcha.chaoxing.com/captcha/get/verification/image"
		params3 = {
			"callback": "cx_captcha_function", "token": token, 
			"captchaId": captcha_id, "captchaKey": captcha_key,
			"type": captcha["type"], "version": "1.1.22",
			"referer": "https://mobilelearn.chaoxing.com",
			"_": _trunc(_time() * 1000), "iv": iv
		}
		res3 = await self.__session.get(url3, params = params3)
		data3 = _loads((await res3.text())[20 : -1])
		img_srcs = data3["imageVerificationVo"]
		captcha.update(
			token = data3["token"], iv = iv,
			context = img_srcs.get("context", ""),
			origin_img_src = img_srcs.get("originImage", ""),
			cutout_img_src = img_srcs.get("cutoutImage", ""),
			shade_img_src = img_srcs.get("shadeImage", "")
		)
		return captcha

	async def captcha_submit_captcha(
		self,
		captcha = {"type": "rotate", "captcha_id": "", "token": "", "iv": "", "vcode": ""}
	):
		"""Submit and verify CAPTCHA.

		:param captcha: CAPTCHA type, ID, token, IV and
		verification code.
		:return: CAPTCHA with validation code on success.
		"""
		url = "https://captcha.chaoxing.com/captcha/check/verification/result"
		params = {
			"callback": "cx_captcha_function",
			"captchaId": captcha["captcha_id"],
			"token": captcha["token"], "iv": captcha["iv"],
			"textClickArr": f"[{{\"x\": {captcha['vcode']}}}]",
			"type": captcha["type"], "coordinate": "[]", "t": "a",
			"version": "1.1.22", "runEnv": 10,
			"_": _trunc(_time() * 1000)
		}
		res = await self.__session.get(url, params = params, headers = {
			**self.__session.headers,
			"Referer": "https://mobilelearn.chaoxing.com"
		})
		return "result\":true" in await res.text(), {
			**captcha, "validate":
			f"validate_{captcha['captcha_id']}_{captcha['token']}"
		}

	async def captcha_handle_captcha(
		self, captcha: dict = {"type": "rotate"}
	):
		"""Get, submit and verify CAPTCHA.

		:param captcha: Same as ``captcha_get_captcha()``. 
		:return: Same as ``captcha_submit_captcha()``.
		"""
		captcha = {**captcha}
		type = captcha["type"]
		if not type in ("rotate", "slide"):
			type = captcha["type"] = "rotate"
		captcha = await self.captcha_get_captcha(captcha = captcha)
		if type == "rotate":
			bi = _create_task(_url_get_img(
				url = captcha["cutout_img_src"], ses = self
			))
			si = await _url_get_img(
				url = captcha["shade_img_src"], ses = self
			)
			bi = await bi
			if not bi or not si:
				return False, captcha
			captcha["vcode"] = _solve_captcha_rotate(
				big_img = bi, small_img = si
			) * 200 // 360
		elif type == "slide":
			bi = _create_task(_url_get_img(
				url = captcha["shade_img_src"], ses = self
			))
			si = await _url_get_img(
				url = captcha["cutout_img_src"], ses = self
			)
			bi = await bi
			if not bi or not si:
				return False, captcha
			captcha["vcode"] = _solve_captcha_slide(
				big_img = bi, small_img = si
			) * 280 // bi.width
		return await self.captcha_submit_captcha(captcha = captcha)

	async def login_username_2(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via Login API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v2()``.
		"""
		url = "https://passport2.chaoxing.com/api/login"
		params = {
			"name": account["username"], "pwd": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.get(
			url, params = params, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			data = await res.json(content_type = None)
			ret.update(
				name = data["realname"],
				cookies = res.cookies, logged_in = True
			)
		return ret

	async def login_username_v2(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V2 API.

		:param account: Username and password in dictionary.
		:return: Name, cookies and login state.
		"""
		url = "https://passport2.chaoxing.com/api/v2/loginbypwd"
		params = {
			"name": account["username"], "pwd": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.get(
			url, params = params, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			data = await res.json(content_type = None)
			ret.update(
				name = data["realname"],
				cookies = res.cookies, logged_in = True
			)
		return ret

	async def login_username_v3(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V3 API.

		:param account: Same as ``login_username_v2()``.
		:return: Name (``""``), cookies and login state.
		"""
		urls = (
			"http://v3.chaoxing.com/vLogin",
			"http://v37.chaoxing.com/v37/vLogin"
		)
		data = {
			"userNumber": account["username"],
			"passWord": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		for url in urls:
			res = await self.__session.post(
				url = url, data = data, allow_redirects = False
			)
			if res.status == 200 and "p_auth_token" in res.cookies:
				ret.update(
					cookies = res.cookies, logged_in = True
				)
				break
		return ret

	async def login_username_v11(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V11 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/v11/loginregister"
		data = {
			"uname": account["username"],
			"code": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, data = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_v21(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V21 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://v21.chaoxing.com/api/login/passport/byPassword"
		data = {
			"phone": _encrypt_aes(
				msg = account["username"],
				key = b"ef352e57323f743d93d925a4dfc312b8",
				mode = _MODE_ECB
			), "password": _encrypt_aes(
				msg = account["password"],
				key = b"ef352e57323f743d93d925a4dfc312b8",
				mode = _MODE_ECB
			)
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, json = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_v24(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V24 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		urls1 = (
			"https://v24.chaoxing.com/cxlmwfwlogin/login",
			"https://v34.chaoxing.com/zsjycwfwlogin/login"
		)
		data1 = {
			"uname": account["username"],
			"password": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		for url1 in urls1:
			res1 = await self.__session.post(
				url = url1, data = data1,
				allow_redirects = False
			)
			if res1.status == 302:
				url2 = _URL(res1.headers[
					"Location"
				]).with_scheme("https")
				res2 = await self.__session.get(
					url2, allow_redirects = False
				)
				if (
					res2.status == 302 and
					"p_auth_token" in res2.cookies
				):
					ret.update(
						cookies = res2.cookies,
						logged_in = True
					)
				break
		return ret

	async def login_username_v25(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V25 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://v25.chaoxing.com/login"
		data = {"name": account["username"], "pwd": account["password"]}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, data = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_v31(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via V31 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://v31.chaoxing.com/zykmicroservice/checkLogin"
		data = {
			"userName": account["username"],
			"password": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, data = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_xxk(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via XXK API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v2()``.
		"""
		url1 = "http://xxk.chaoxing.com/api/front/user/login"
		data1 = {
			"username": account["username"], 
			"password": account["password"], "numcode": 0
		}
		res1 = await self.__session.post(
			url = url1, data = data1, allow_redirects = False
		)
		ret = {"name": "", "cookies": None, "logged_in": False}
		if "p_auth_token" in res1.cookies:
			res1.cookies["UID"] = res1.cookies["_uid"]
			ret = await self.login_cookies(account = {"cookies": {
				k: v.value for k, v in res1.cookies.items()
			}})
		return ret

	async def login_username_xxt(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via XXT API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/xxt/loginregisternew"
		params = {
			"uname": account["username"],
			"code": account["password"]
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.get(
			url, params = params, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(
				name = "", cookies = res.cookies,
				logged_in = True
			)
		return ret

	async def login_username_mylogin1(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via Mylogin1 API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/mylogin1"
		data = {
			"fid": "undefined", "msg": account["username"], 
			"vercode": account["password"], "type": 1
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, data = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_fanya(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via Fanya API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/fanyalogin"
		data = {
			"uname": _encrypt_aes(
				msg = account["username"],
				key = b"u2oh6Vu^HWe4_AES",
				iv = b"u2oh6Vu^HWe4_AES"
			), "password": _encrypt_aes(
				msg = account["password"],
				key = b"u2oh6Vu^HWe4_AES",
				iv = b"u2oh6Vu^HWe4_AES"
			), "t": True
		}
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.post(
			url = url, data = data, allow_redirects = False
		)
		if res.status == 200 and "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_username_yz(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password
		via Yunzhou API.

		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		ret = {"name": "", "cookies": None, "logged_in": False}
		url1 = "https://yz.chaoxing.com"
		res1 = await self.__session.get(url1, allow_redirects = False)
		if res1.status != 200:
			return ret
		match = _Chaoxing_login_username_yz_regex.search(
			await res1.text()
		)
		if not match:
			return ret
		url2 = "https://yz.chaoxing.com/login6"
		data2 = {
			"enc": match[1], "uname": account["username"],
			"password": account["password"]
		}
		res = await self.__session.post(
			url2, data2, allow_redirects = False
		)
		if "p_auth_token" in res.cookies:
			ret.update(cookies = res.cookies, logged_in = True)
		return ret

	async def login_cookies(self, account: dict = {"cookies": None}):
		"""Log into Chaoxing account with cookies.

		:param account: Cookies in dictionary.
		:return: Same as ``login_username_v2()``.
		"""
		url = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
		ret = {"name": "", "cookies": None, "logged_in": False}
		res = await self.__session.get(
			url, cookies = account["cookies"],
			allow_redirects = False
		)
		if res.status == 200:
			data = await res.json(content_type = None)
			if data["result"]:
				ret.update(
					name = data["msg"]["name"],
					cookies = res.cookies, logged_in = True
				)
		return ret

	async def curriculum_get_curriculum(self, week: str = ""):
		"""Get curriculum.

		:param week: Week number. Defaulted to the current week.
		:return: Dictionary of curriculum details and lessons containing
		course IDs, names, classroom names, teachers and time.
		"""
		def _add_lesson(lesson):
			class_id = f"{lesson['classId']}"
			lesson = {
				"class_id": class_id,
				"course_id": f"{lesson['courseId']}",
				"name": lesson["name"],
				"classrooms": [lesson["location"]],
				"invite_code": lesson["meetCode"],
				"teachers": [lesson["teacherName"]],
				"times": [{
					"day": f"{lesson['dayOfWeek']}",
					"period_begin":
					f"{lesson['beginNumber']}",
					"period_end": f"""{
						lesson['beginNumber'] +
						lesson['length'] - 1
					}"""
				}]
			}
			if not class_id in curriculum["lessons"]:
				curriculum["lessons"][class_id] = lesson
				return
			_lesson = curriculum["lessons"][class_id]
			if not lesson["classrooms"][0] in _lesson["classrooms"]:
				_lesson["classrooms"].append(
					lesson["classrooms"][0]
				)
			if not lesson["teachers"][0] in _lesson["teachers"]:
				_lesson["teachers"].append(
					lesson["teachers"][0]
				)
			if not lesson["times"][0] in _lesson["times"]:
				_lesson["times"].append(lesson["times"][0])
		url = "https://kb.chaoxing.com/curriculum/getMyLessons"
		params = {
			"week": week
		}
		res = await self.__session.get(
			url, params = params, ttl = 21600
		)
		data = (await res.json()).get("data")
		details = data["curriculum"]
		curriculum = {
			"details": {
				"year": f"{details['schoolYear']}",
				"semester": f"{details['semester']}",
				"week": f"{details['currentWeek']}",
				"week_real": f"{details['realCurrentWeek']}",
				"week_max": f"{details['maxWeek']}",
				"time": {
					"period_max": f"{details['maxLength']}",
					"timetable":
					details["lessonTimeConfigArray"][ : -1]
				}
			}, "lessons": {}
		}
		lessons = data.get("lessonArray") or []
		for lesson in lessons:
			_add_lesson(lesson = lesson)
			for conflict in lesson.get("conflictLessons") or {}:
				_add_lesson(lesson = conflict)
		return curriculum

	async def course_get_meeting_courses(self):
		"""Get all active meeting courses.

		:return: Dictionary of class IDs to courses containing
		course IDs, names, teachers, status, start and end time.
		"""
		url = "https://k.chaoxing.com/pc/meet/index_mymeet_v2"
		params = {"pageSize": 20, "offsetUpdateTime": ""}
		time = _time() * 1000
		courses_limit = self.__config[
			"chaoxing_course_get_activities_courses_limit"
		]
		courses = {}
		while True:
			res = await self.get(url, params = params, ttl = 21600)
			d = (await res.json())["data"]
			meetings = d["listData"]
			for meeting in meetings:
				if not meeting["temFlag"] or meeting["isTeach"]:
					continue
				for course in meeting["meetClasses"]:
					if (course[
						"reserveEndTime"
					] or float("inf")) < time or course[
						"meetCurStatus"
					] == 1:
						continue
					class_id = f"{course['id']}"
					time_start = course["reserveStartTime"]
					time_end = course["reserveEndTime"]
					courses[class_id] = {
						"class_id": class_id,
						"course_id":
						f"{course['courseId']}",
						"name": course["title"],
						"teachers": [course[
							"createrName"
						]], "status": 1,
						"time_start": _strftime(
							time_start // 1000
						) if time_start else "",
						"time_end": _strftime(
							time_end // 1000
						) if time_end else ""
					}
					if 0 < courses_limit <= len(courses):
						break
			if d["lastPage"]:
				break
			params["offsetUpdateTime"] = meetings[-1]["updateTime"]
		return courses

	async def course_get_courses(self):
		"""Get all active courses in the root folder.

		:return: Dictionary of class IDs to courses containing
		course IDs, names, teachers, status, start and end time.
		"""
		urls = [
			"https://mooc-res1.chaoxing.com/visit/courselistdata",
			"https://mooc-res1-gray.chaoxing.com/visit/courselistdata",
			"https://mooc-res2-gray.chaoxing.com/visit/courselistdata",
			"https://mooc1-1.chaoxing.com/visit/courselistdata",
			"https://mooc1-2.chaoxing.com/visit/courselistdata",
			"https://mooc1-3.chaoxing.com/visit/courselistdata",
			"https://mooc1-4.chaoxing.com/visit/courselistdata",
			"https://mooc1-api.chaoxing.com/visit/courselistdata",
			"https://mooc1.emooc.xidian.edu.cn/visit/courselistdata",
			"https://mooc1-gray.chaoxing.com/visit/courselistdata",
			"https://mooc2-ans.chaoxing.com/visit/courselistdata",
			"https://mooc2-ans.emooc.xidian.edu.cn/visit/courselistdata",
			"https://mooc2-gray.chaoxing.com/visit/courselistdata"
		]
		_shuffle(urls)
		params = {"courseType": 1}
		matches = None
		cookies = {
			k: v.value for k, v in self.__session.cookies.items()
		}
		for url in urls:
			headers = self.__session.headers.copy()
			if url.startswith("https://mooc2-gray"):
				headers.update({
					"X-Requested-With": "XMLHttpRequest",
					"Origin":
					"https://mooc2-gray.chaoxing.com",
					"Referer":
					"https://mooc2-gray.chaoxing.com"
				})
			res = await self.__session.get(
				url, params = params, headers = headers,
				cookies = cookies, ttl = 21600
			)
			matches = _Chaoxing_course_get_courses_regex1.findall(
				await res.text()
			)
			if matches:
				break
		courses_limit = self.__config[
			"chaoxing_course_get_activities_courses_limit"
		]
		courses = {}
		status = 1
		for match in matches:
			if 0 < courses_limit <= len(courses) or match[2]:
				status = 0
				break
			courses[match[1]] = {
				"class_id": match[1], "course_id": match[0],
				"name": match[3], "teachers": 
				_Chaoxing_course_get_courses_regex2.split(
					match[4]
				), "status": status, "time_start":
				f"{match[5]} 00:00:00" if match[5] else "",
				"time_end":
				f"{match[6]} 00:00:00" if match[6] else ""
			}
		return courses

	async def course_get_course_id(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get course ID of a course.

		:param course: Course ID (optional) and clsss ID.
		:return: Course ID corresponding to the class ID.
		"""
		class_id = course["class_id"]
		course_id = course.get("course_id")
		if course_id:
			return course_id
		if class_id in self.__secrets["courses"]:
			return self.__secrets["courses"][class_id]["course_id"]
		url = "https://mobilelearn.chaoxing.com/v2/apis/class/getClassDetail"
		params = {"courseId": "", "classId": class_id}
		res = await self.__session.get(
			url, params = params, ttl = 2592000
		)
		data = (await res.json()).get('data')
		if data:
			return f"{data['courseid']}"
		return "0"

	async def course_get_location_log(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get checkin location history of a course.

		:param course: Course ID (optional) and class ID.
		:return: Dictionary of activity IDs to checkin locations
		used by the course.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/sign/getLocationLog"
		params = {
			"DB_STRATEGY": "COURSEID", "STRATEGY_PARA": "courseId",
			"courseId":
			await self.course_get_course_id(course = course),
			"classId": course["class_id"]
		}
		res = await self.__session.get(url, params = params, ttl = 1800)
		data = (await res.json()).get("data") or []
		return {
			location["activeid"]: {
				"latitude": location["latitude"],
				"longitude": location["longitude"],
				"address": location["address"],
				"ranged": 1,
				"range": int(location["locationrange"])
			} for location in data
		}

	async def course_get_course_activities_v2(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get activities of a course via V2 API.

		:param course: Course ID (optional) and class ID.
		:return: List of ongoing activities with type, name,
		activity ID, start, end and remaining time.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
		params = {
			"fid": "1", "classId": course["class_id"],
			"courseId":
			await self.course_get_course_id(course = course),
			"showNotStartedActive": 0
		}
		res = await self.__session.get(url, params = params, ttl = 30)
		data = ((await res.json()).get("data") or {}).get(
			"activeList"
		) or []
		return [
			{
				"active_id": f"{activity['id']}",
				"type": activity["otherId"],
				"name": activity["nameOne"],
				"time_start":
				_strftime(activity["startTime"] // 1000),
				"time_end":
				_strftime(activity["endTime"] // 1000)
				if activity["endTime"] else "",
				"time_left": activity["nameFour"]
			} for activity in data if (
				activity["status"] == 1 and
				activity.get("otherId") in ("2", "4")
			)
		]

	async def course_get_course_activities_ppt(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get activities of a course via PPT API.
		Meeting courses are not supported.

		:param course: Course ID (optional) and class ID.
		:return: List of ongoing activities with type, name,
		activity ID, start, end and remaining time.
		"""
		url = "https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist"
		params = {
			"classId": course["class_id"], "courseId":
			await self.course_get_course_id(course = course),
			"showNotStartedActive": 0
		}
		res = await self.__session.get(url, params = params, ttl = 30)
		data = (await res.json(
			content_type = None
		)).get("activeList") or []
		if not data:
			return
		all_details = {}
		_sem = _Semaphore(self.__config[
			"chaoxing_course_get_activities_workers"
		])
		async def _get_details(active_id):
			a = {"active_id": f"{active_id}"}
			async with _sem:
				all_details[
					active_id
				] = await self.checkin_get_info_widget(
					activity = a
				)
		await _gather(*(
			_get_details(activity["id"]) for activity in data
			if activity["status"] == 1 and
			activity["activeType"] == 2
		))
		activities = []
		for activity in data:
			if (
				activity["status"] != 1 or
				activity["activeType"] != 2
			):
				continue
			details = all_details[activity["id"]]
			if not details["otherId"] in (2, 4):
				continue
			activities.append({
				"active_id": f"{activity['id']}",
				"type": f"{details['otherId']}",
				"name": activity["nameOne"],
				"time_start": details["starttimeStr"],
				"time_end": details["endtimeStr"] or "",
				"time_left": activity["nameFour"]
			})
		return activities

	async def course_get_activities(self):
		"""Get activities of all courses.

		:return: Dictionary of Class IDs to ongoing activities.
		"""
		url = "https://ketang-zhizhen.chaoxing.com/education/student/activelist"
		params = {
			"startTimeSet": "", "statusSet": 1, "devices": 0,
			"includeWork": 0, "includeExam": 0, "includeRead": 0
		}
		activities = {}
		async def _worker():
			while True:
				res = await self.__session.get(
					url, params = params, ttl = 30
				)
				data = ((await res.json(
					content_type = None
				)).get("data") or {}).get("array") or []
				for activity in data:
					class_id = f"{activity['classId']}"
					if activity[
						"activeType"
					] != 2 or not activity[
						"otherId"
					] in ("2", "4") or (
						self.__courses and
						not class_id in self.__courses
					):
						continue
					start = activity["startTime"]
					end = activity["endTime"]
					activities.setdefault(
						class_id, []
					).append({
						"active_id":
						f"{activity['id']}",
						"type": activity["otherId"],
						"name": activity["nameOne"],
						"time_start": _strftime(
							start // 1000
						), "time_end": _strftime(
							end // 1000
						) if end else "", "time_left":
						activity["nameFour"]
					})
				if len(data) < 20:
					break
				params["startTimeSet"] = data[-1]["startTime"]
		_tworker = _create_task(_worker())
		_sem = _Semaphore(self.__config[
			"chaoxing_course_get_activities_workers"
		])
		async def _mworker(course):
			async with _sem:
				a = await self.course_get_course_activities_v2(
					course = course
				)
			if a:
				activities[course["class_id"]] = a
		await _gather(*(_mworker(
			course
		) for course in self.__meeting_courses.values()))
		await _tworker
		return activities

	async def checkin_get_info_newsign(
		self, activity: dict = {"active_id": ""}
	):
		"""Get checkin details via Newsign API.

		:param activity: Activity ID.
		:return: Checkin details on success.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/signDetail"
		params = {"activePrimaryId": activity["active_id"], "type": 1}
		res = await self.__session.get(url, params = params, ttl = 60)
		return (await res.json(content_type = None)) or {}

	async def checkin_get_info_ppt(
		self, activity: dict = {"active_id": ""}
	):
		"""Get checkin details via PPT API.
		:param activity: Activity ID.
		:return: Checkin details on success.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo"
		params = {"activeId": activity["active_id"]}
		res = await self.__session.get(url, params = params, ttl = 60)
		return (await res.json()).get("data") or {}

	async def checkin_get_info_widget(
		self, activity: dict = {"active_id": ""}
	):
		"""Get checkin details via Widget API.

		:param activity: Activity ID.
		:return: Checkin details on success.
		"""
		url = "https://mobilelearn.chaoxing.com/widget/active/getActiveInfo"
		params = {"id": activity["active_id"]}
		res = await self.__session.get(url, params = params, ttl = 60)
		return (
			(await res.json()).get("data") or {}
		).get("detail") or {}

	def checkin_format_location(
		self,
		location: dict = {"latitude": -1, "longitude": -1, "address": ""},
		new_location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Format checkin location.

		:param location: Address, latitude and longitude.
		Used to override address for checkin location.
		:param location_new: Address, latitude and longitude.
		The checkin location to upload.
		:return: Checkin location containing address, latitude,
		longitude, range and ranged flag.
		"""
		new_location = {"ranged": 0, "range": 0, **new_location}
		_rand = lambda x: round(x - 0.0005 + _uniform(0, 0.001), 6)
		if self.__config["chaoxing_checkin_location_randomness"]:
			new_location.update(
				latitude = _rand(new_location["latitude"]),
				longitude = _rand(new_location["longitude"])
			)
		if len(new_location["address"]) < self.__config[
			"chaoxing_checkin_location_address_override_maxlen"
		]:
			new_location["address"] = location["address"]
		return new_location

	async def checkin_get_location(
		self, activity: dict = {"active_id": ""},
		course: dict ={"course_id": "", "class_id": ""}
	):
		"""Get checkin location from the location log of its
		corresponding course.
		:param activity: Activity ID in dictionary.
		:param course: Course ID (optional) and class ID.
		:return: Checkin location containing address, latitude,
		longitude, range and ranged flag.
		"""
		locations = await self.course_get_location_log(course = course)
		return locations.get(
			activity["active_id"], next(iter(locations.values()))
		) if locations else {
			"latitude": -1, "longitude": -1, "address": "",
			"ranged": 0, "range": 0
		}

	async def checkin_get_location_error(
		self, activity: dict = {"active_id": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": ""},
		error = "errorLocation1"
	):
		"""Get checkin location on error checking-in with the
		previous location.
		:param activity: Activity ID in dictionary.
		:param course: Course ID (optional) and class ID.
		:param location: Address, latitude and longitude.
		:param error: Error message returned.
		:return: The new checkin location containing address, latitude,
		longitude, range and ranged flag. Falls back to the given one
		on failure.
		"""
		url = "https://mobilelearn.chaoxing.com/pptSign/errorLocation"
		params = {
			"DB_STRATEGY": "PRIMARY_KEY",
			"STRATEGY_PARA": "activeId", "uid": self.__uid,
			"activeId": activity["active_id"], "errortype": error,
			"location": _dumps({
				"mockData": {"probability": 0},
				"result": 1, "address": location["address"],
				"latitude": location["latitude"],
				"longitude": location["longitude"]
			})
		}
		res = await self.__session.get(url, params = params, ttl = 60)
		if not res.status == 200:
			return location
		match = _Chaoxing_checkin_get_location_error_regex.search(
			await res.text()
		)
		if match:			
			location = {
				"latitude":
				float(match[3] or location["latitude"]),
				"longitude":
				float(match[4] or location["longitude"]),
				"address": match[2] or location["address"],
				"ranged": int(match[1]),
				"range": int(match[5] or 0)
			}
		return location

	async def checkin_do_analysis(self, activity: dict = {"active_id": ""}):
		"""Send analytics for checkin.

		:param activity: Activity ID in dictionary.
		:return: ``True`` on success.
		"""
		url1 = "https://mobilelearn.chaoxing.com/pptSign/analysis"
		params1 = {
			"vs": 1, "DB_STRATEGY": "RANDOM",
			"aid": activity["active_id"]
		}
		res1 = await self.__session.get(
			url1, params = params1, ttl = 1800
		)
		if res1.status != 200:
			return False
		url2 = "https://mobilelearn.chaoxing.com/pptSign/analysis2"
		params2 = {
			"code": _Chaoxing_checkin_do_analysis_regex.search(
				await res1.text()
			)[1], "DB_STRATEGY": "RANDOM"
		}
		res2 = await self.__session.get(
			url2, params = params2, ttl = 1800
		)
		return await res2.text() == "success"

	async def checkin_do_presign(
		self, activity: dict = {"active_id": ""},
		course: dict ={"course_id": "", "class_id": ""}
	):
		"""Do checkin pre-sign.

		:param activity: Activity ID in dictionary.
		:param course: Course ID (optional) and class ID.
		:return: Presign state (``2`` if checked-in or ``1`` on success)
		and checkin location.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/preSign"
		params = {
			"general": 1, "sys": 1, "ls": 1, "appType": 15,
			"ut": "s", "uid": self.__uid, "tid": (
				self.__session.cookies["_tid"].value
				if "_tid" in self.__session.cookies else 0
			), "classId": course["class_id"], "courseId":
			await self.course_get_course_id(course = course),
			"activePrimaryId": activity["active_id"]
		}
		location = {
			"latitude": -1, "longitude": -1, "address": "",
			"ranged": 0, "range": 0
		}
		res = await self.__session.get(url, params = params)
		if res.status != 200:
			return 0, location
		state = 1
		match = _Chaoxing_checkin_do_presign_regex.search(
			await res.text()
		)
		if match:
			if match[6]:
				state = 2
			if match[1] == "1":
				location = {
					"latitude": float(match[3] or -1),
					"longitude": float(match[4] or -1),
					"address": match[2] or "",
					"ranged": int(match[1]),
					"range": int(match[5] or 0)
				}
		return state, location

	async def checkin_do_sign(
		self, activity: dict = {"active_id": "", "type": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": "", "ranged": 0},
		old_params: dict = {"name": "", "uid": "", "fid": "", "...": "..."}
	):
		"""Do checkin sign.

		:param activity: Activity ID and type in dictionary.
		:param location: Address, latitude, longitude and ranged flag.
		:param old_params: Reuse previous parameters.
		Overrides activity and location if given.
		:return: Sign state (``True`` on success), message
		and parameters.
		"""
		def _update_params(params, activity, location):
			if activity["type"] == "4":
				params.update(
					address = location["address"],
					latitude = location["latitude"],
					longitude = location["longitude"],
					ifTiJiao = location["ranged"],
					vpProbability = -1
				)
			elif activity["type"] == "2":
				if location["ranged"]:
					params.update(location = _dumps({
						"mockData": {"probability": 0},
						"result": 1, "address":
						location["address"],
						"latitude":
						location["latitude"],
						"longitude":
						location["longitude"]
					}), ifTiJiao = location["ranged"])
				else:
					params.update(
						address = location["address"],
						latitude = location["latitude"],
						longitude =
						location["longitude"]
					)
		async def _do_sign(activity, location, old_params):
			if old_params.get("activeId"):
				params = old_params
				activity = {
					"active_id": old_params["activeId"],
					"type":
					(await self.checkin_get_info_widget(
						activity = activity
					))["otherId"]
				}
			else:
				params = {
					"name": "", "uid": self.__uid,
					"fid": self.__fid,
					"activeId": activity["active_id"],
					"enc": activity.get("enc", ""),
					"enc2": "", "address": "",
					"latitude": -1, "longitude": -1,
					"location": "", "ifTiJiao": 0,
					"clientip": "", "validate": "",
					"appType": 15, "deviceCode":
					self.__secrets["device_code"],
					"vpProbability": "", "vpStrategy": ""
				}
				_update_params(
					params = params, activity = activity,
					location = location
				)
			url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax"
			res = await self.__session.get(url, params = params)
			text = await res.text()
			if "errorLocation" in text:
				_update_params(
					params = params, activity = activity,
					location =
					await self.checkin_get_location_error(
						activity = activity,
						location = location,
						error = text
					)
				)
				res = await self.__session.get(
					url, params = params
				)
				text = await res.text()
			status = False
			if text in ("success", "您已签到过了"):
				status = True
				msg = f"Checkin success. ({text})"
			elif "validate" in text:
				match = _Chaoxing_checkin_do_sign_regex.search(
					text
				)
				if match:
					params["enc2"] = match[1]
				msg = f"Checkin validation. ({text})"
			else:
				msg = f"Checkin failure. ({text})"
			return status, msg, params
		status, msg, params = await _do_sign(
			activity, location, old_params
		)
		if not status and "validate" in msg:
			for _ in range(3):
				r, captcha = (await self.captcha_handle_captcha(
					captcha = {"type": "rotate"}
				))
				if not r:
					continue
				params["validate"] = captcha["validate"]
				status, msg, params = (
					await _do_sign(
						activity, location, params
					)
				)
				if status:
					break
		return status, {"msg": msg, "params": params}

	async def checkin_checkin_location(
		self, activity: dict = {"active_id": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Location checkin.

		:param activity: Activity ID in dictionary.
		:param location: Address, latitude and longitude.
		Overriden by server-side location if any.
		:return: Checkin state (``True`` on success), message
		and parameters.
		"""
		try:
			_analyze = _create_task(self.checkin_do_analysis(
				activity = activity
			))
			info = await self.checkin_get_info_widget(
				activity = activity
			)
			assert (
				info["status"] == 1 and not info["isdelete"]
			), "Activity ended or deleted."
			course = {"class_id": f"{info['clazzid']}"}
			presign = await self.checkin_do_presign(
				activity = activity, course = course
			)
			assert (
				presign[0]
			), f"Presign failure. {activity, presign}"
			if presign[0] == 2:
				return True, {
					"params": {}, "captcha": {}, "msg":
					"Checkin success. (Already checked in.)"
				}
			content = _loads(info["content"])
			location = self.checkin_format_location(
				location = location, new_location = {
					"ranged": 1, "latitude":
					float(content["locationLatitude"]),
					"longitude":
					float(content["locationLongitude"]),
					"address": content["locationText"]
				}
			) if content["ifopenAddress"] else {
				**location, "ranged": 0
			}
			await _analyze
			result = await self.checkin_do_sign(
				activity = {**activity, "type": "4"},
				location = location
			)
			return result
		except Exception as e:
			return False, {"msg": f"{e}", "params": {}}

	async def checkin_checkin_qrcode(
		self, activity: dict = {"active_id": "", "enc": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Qrcode checkin.

		:param activity: Activity ID and ENC in dictionary.
		:param location: Same as ``checkin_checkin_location()``.
		:return: Same as ``checkin_checkin_location()``.
		"""
		try:
			_analyze = _create_task(self.checkin_do_analysis(
				activity = activity
			))
			info = await self.checkin_get_info_widget(
				activity = activity
			)
			assert (
				info["status"] == 1 and not info["isdelete"]
			), "Activity ended or deleted."
			course = {"class_id": f"{info['clazzid']}"}
			presign = await self.checkin_do_presign(
				activity = activity, course = course
			)
			assert (
				presign[0]
			), f"Presign failure. {activity, presign}"
			if presign[0] == 2:
				return True, {
					"params": {}, "captcha": {}, "msg":
					"Checkin success. (Already checked in.)"
				}
			content = _loads(info["content"])
			location = self.checkin_format_location(
				location = location, new_location = {
					"ranged": 1, "latitude":
					float(content["locationLatitude"]),
					"longitude":
					float(content["locationLongitude"]),
					"address": content["locationText"]
				}
			) if content.get("ifopenAddress") else {
				**location, "ranged": 0
			}
			await _analyze
			result = await self.checkin_do_sign(
				activity = {**activity, "type": "2"},
				location = location
			)
			return result
		except Exception as e:
			return False, {"msg": f"{e}", "params": {}}

	async def checkin_checkin_qrcode_url(
		self, url: str = "",
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Qrcode checkin.

		:param url: URL from Qrcode.
		:param location: Same as ``checkin_checkin_location()``.
		:return: Same as ``checkin_checkin_location()``.
		"""
		match = _Chaoxing_checkin_checkin_qrcode_url_regex.search(url)
		try:
			return await self.checkin_checkin_qrcode(activity = {
				"active_id": match[1], "enc": match[2]
			}, location = location)
		except Exception as e:
			return False, {"msg": f"{e}", "params": {}}
