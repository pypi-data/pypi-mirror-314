# -*- coding: utf-8 -*-

__all__ = ("Cldisk", )

from asyncio import create_task as _create_task
from io import BytesIO as _BytesIO
from math import trunc as _trunc
from re import compile as _compile, DOTALL as _DOTALL
from time import time as _time
from aiohttp import FormData as _FormData, request as _request
from xdcheckin.core.chaoxing import Chaoxing as _Chaoxing, _Chaoxing_config_base
from xdcheckin.util.time import strftime as _strftime

_Cldisk_pan_get_root_regex = _compile(r"\"node_root\" nodeid=\"(\d+)_(\d+)\"")
_Cldisk_pan_share_share_regex = _compile(
	r"(https://.*?/share/info/([0-9a-z]{16}))?.*?(result\":true)?"
)
_Cldisk_pan_file_info_res_id_regex = _compile(r"objectId': '([0-9a-z]{32})")
_Cldisk_pan_file_download_res_id_regex = _compile(
	r"fileinfo = {\s+'download':  '(.*?)' ,", _DOTALL
)

class Cldisk:
	"""Chaoxing clouddisk APIs.
	"""
	__async_ctxmgr = __cx = __secrets = None
	__logged_in = False

	def __init__(self, chaoxing: _Chaoxing = None):
		"""Create a Cldisk with ``Chaoxing`` instance.

		:param chaoxing: The ``Chaoxing`` instance.
		"""
		if not self.__async_ctxmgr is None:
			return
		self.__cx = chaoxing
		self.__secrets = {}

	async def __aenter__(self):
		if not self.__async_ctxmgr is None:
			return self
		self.__async_ctxmgr = True
		await self.__cx.__aenter__()
		if self.__cx.logged_in:
			self.__logged_in = True
		async def _get_token():
			self.__secrets[
				"clouddisk_token"
			] = await self.pan_get_token()
		t_get_token = _create_task(_get_token())
		self.__secrets["clouddisk_root"] = await self.pan_get_root()
		await t_get_token
		return self

	async def __aexit__(self, *args, **kwargs):
		if not self.__async_ctxmgr:
			return
		self.__logged_in = False
		self.__async_ctxmgr = False

	async def get(self, *args, **kwargs):
		return await self.__cx.get(*args, **kwargs)

	async def post(self, *args, **kwargs):
		return await self.__cx.post(*args, **kwargs)

	@property
	def logged_in(self):
		return self.__logged_in

	async def pan_get_token(self):
		"""Get token for the clouddisk.

		:return: The token.
		"""
		url = "https://pan-yz.chaoxing.com/api/token/uservalid"
		res = await self.__cx.get(url, ttl = 2592000)
		return (await res.json(content_type = None))["_token"]

	async def pan_get_root(self):
		"""Get root folder of the clouddisk.

		:return: File information containing name and resource ID.
		"""
		url = "https://pan-yz.chaoxing.com/foldertreenew"
		res = await self.__cx.get(url, ttl = 2592000)
		file = {"name": "", "res_id": ""}
		if res.status == 200:
			file.update(await self.pan_file_info({
				"res_id": _Cldisk_pan_get_root_regex.search(
					await res.text()
				)[1]
			}))
			file["name"] = f"_root_pisnull_{self.__cx.uid}"
		return file

	async def pan_get_info(self):
		"""Get information about the clouddisk.

		:return: Disk usage and capacity.
		"""
		url = "https://pan-yz.chaoxing.com/api/info"
		params = {
			"puid": self.__cx.uid,
			"_token": self.__secrets["clouddisk_token"]
		}
		res = await self.__cx.get(url, params = params, ttl = 60)
		d = (await res.json(content_type = None))["data"]
		return {"size_used": d["usedsize"], "size_total": d["disksize"]}

	async def pan_recycle_list(self, page_no: int = 1, page_size: int = 64):
		"""List folders and files in the recycle bin.

		:param page_no: Page number for listing.
		:param page_size: Page size for listing.
		:return: Resource ID to folders and files.
		"""
		url = "https://pan-yz.chaoxing.com/recycle"
		params = {"page": page_no, "size": page_size}
		res = await self.__cx.post(url, params = params)
		d = (await res.json(content_type = None)).get("data", [])
		return {v["id"]: {
			"name": v["name"],
			"type": v["resTypeValue"], "size": v["size"],
			"time_upload": _strftime(v["uploadDate"] // 1000),
			"time_modify": _strftime(v["modifyDate"] // 1000),
			"res_id": v["id"], "crc": v.get("crc", ""),
			"encrypted_id": v["encryptedId"],
			"creator_uid": f"{v['creator']}"
		} for v in d}

	async def pan_recycle_recover(self, file: dict = {"res_id": ""}):
		"""Recover folder or file from the recycle bin.

		:param file: Resource ID in dictionary.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/recycle/recover"
		data = {"resids": file["res_id"], "t": 0}
		res = await self.__cx.post(url, data = data)
		return res.status == 200

	async def pan_recycle_delete(self, file: dict = {"res_id": ""}):
		"""Delete folder or file from the recycle bin.

		:param file: Resource ID in dictionary.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/recycle/delres"
		params = {"resids": file["res_id"]}
		res = await self.__cx.post(url, params = params)
		return (await res.json(
			content_type = None
		))["success"] if res.status == 200 else False

	async def pan_share_share(
		self, file: dict = {"res_id": "", "object_id": ""}
	):
		"""Share folder or file from the clouddisk.

		:param file: Resource ID or object ID in dictionary.
		:return: File information with share string (for folder) and
		share URL on success.
		"""
		ret = file.copy()
		m = None
		if file.get("res_id"):
			url = "https://pan-yz.chaoxing.com/forward/getAttachmentData"
			params = {"resid": file["res_id"]}
			res = await self.__cx.get(url, params = params)
			m = _Cldisk_pan_share_share_regex.search(
				await res.text()
			)
		if m and m[2]:
			ret.update(share_str = m[1], share_url = m[0])
		else:
			ret.update(
				share_str = "", share_url =
				f"""https://pan-yz.chaoxing.com/external/m/file{
					file.get('res_id') or
					file.get('object_id')
				}"""
			)
		return ret

	async def pan_share_list(
		self, parent: dict = {"share_str": "", "res_id": ""},
		page_no: int = 1, page_size: int = 64
	):
		"""List folder shared from the clouddisk.

		:param parent: Share string and Resource ID (optional).
		Resource ID is needed for listing subfolders under the share.
		:param page_no: Page number for listing.
		:param page_size: Page size for listing.
		:return: Resource ID to folders and files.
		"""
		url = "https://pan-yz.chaoxing.com/share/info/content"
		data = {
			"page": page_no, "size": page_size,
			"str": parent["share_str"], "fldid":
			parent.get("res_id", "")
		}
		res = await self.__cx.post(url, data = data)
		d = (await res.json(
			content_type = None
		)).get("data", []) if res.status == 200 else []
		return {v["id"]: {
			"name": v["name"],
			"type": v["resTypeValue"], "size": v["filesize"],
			"time_upload": _strftime(v["uploadDate"] // 1000),
			"time_modify": _strftime(v["modifyDate"] // 1000),
			"res_id": v["id"], "crc": v.get("crc", ""),
			"encrypted_id": v["encryptedId"],
			"creator_uid": f"{v['creator']}"
		} for v in d}

	async def pan_share_save(
		self,
		file: dict = {"res_id": "", "creator_uid": "", "object_id": ""},
		parent: dict = {"res_id": ""}
	):
		"""Save shared folder or file to the clouddisk.

		:param file: Resource ID and creator UID or object ID.
		:param parent: Resource ID of the destination folder. Optional.
		:return: True on success.
		"""
		if file.get("res_id") and file.get("creator_uid"):
			url = "https://pan-yz.chaoxing.com/pcNote/allsave"
			params = {
				"srcPuid": file["creator_uid"],
				"srcFileId": file["res_id"],
				"destFileId": parent["res_id"]
			}
		else:
			url = "https://pan-yz.cldisk.com/external/saveToUserPan"
			params = {
				"objectid": file["object_id"], "folderid":
				f"{parent['res_id']}_{self.__cx.uid}",
				"resid": -1
			}
		res = await self.__cx.get(url, params = params)
		return res.status == 200 and (await res.json(
			content_type = None
		))["result"]

	async def pan_folder_create_or_rename(
		self, file: dict = {"res_id": "", "name": ""},
		parent: dict = {"res_id": ""}
	):
		"""Create or rename folder in the clouddisk.

		:param file: Resource ID (optional) and folder name (optional).
		New folder will be created if the ID is not given.
		:param parent: Resource ID of the parent folder. Optional.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/opt/newRootfolder"
		data = {
			"cx_p_token": self.__cx.cookies["cx_p_token"],
			"newfileid": file.get("res_id", "0"),
			"selectDlid": "onlyme", "name": file.get(
				"name", 
	    			f"cldisk-upload-{_trunc(_time() * 1000)}"
			), "parentId": parent.get(
				"res_id", ""
			) if file.get("res_id") else ""
		}
		res = await self.__cx.post(url, data = data)
		return (await res.json(
			content_type = None
		))["success"] if res.status == 200 else False

	async def pan_file_list(
		self, parent: dict = {"res_id": ""}, folder_only: bool = False,
		page_no: int = 1, page_size: int = 64
	):
		"""List folders and files in a folder.

		:param parent: Resource ID in dictionary. Empty by default
		for the root. Optional if ``folder_only`` is ``False``.
		:param folder_only: Whether only to list folders.
		:param page_no: Page number for listing.
		:param page_size: Page size for listing.
		:return: Resource ID to folders and files.
		"""
		url = (
			"https://pan-yz.chaoxing.com/opt/listfolder"
			if folder_only else
			"https://pan-yz.chaoxing.com/api/getMyDirAndFiles"
		)
		params = {"puid": self.__cx.uid}
		if folder_only:
			params.update(parentId = parent.get("res_id", ""))
		else:
			params.update(
				fldid = parent.get("res_id", ""),
				_token = self.__secrets["clouddisk_token"],
				page = page_no, size = page_size,
				orderby = "d", order = "desc"
			)
		res = await self.__cx.post(url, params = params)
		d = (await res.json(
			content_type = None
		)).get("data", []) if res.status == 200 else []
		return {v["residstr"]: {
			"name": v["name"],
			"type": v["resTypeValue"], "size": v["size"],
			"time_upload": _strftime(v["uploadDate"] // 1000),
			"time_modify": _strftime(v["modifyDate"] // 1000),
			"res_id": v["residstr"], "crc": v.get("crc", ""),
			"encrypted_id": v["encryptedId"],
			"creator_uid": f"{v['creator']}"
		} for v in d}

	@staticmethod
	async def pan_file_info_object_id(
		file: dict = {"object_id": ""}, self = None
	):
		"""Get a file's information in the clouddisk
		with object ID anonymously.

		:param file: Object ID in dictionary.
		:param self: ``Cldisk`` instance. Optional.
		:return: File information containing name and download URL.
		"""
		url = f"https://mooc1.chaoxing.com/ananas/status/{file['object_id']}"
		headers = {
			**_Chaoxing_config_base["requests_headers"],
			"Referer": "https://mooc1.chaoxing.com"
		}
		d = None
		if self:
			res = await self.get(url, headers = headers)
			if res.status == 200:
				d = await res.json()
		else:
			async with _request(
				"GET", url, headers = headers
			) as res:
				if res.status == 200:
					d = await res.json()
		ret = {"name": "", "object_id": ""}
		if d:
			ret.update(
				name = d["filename"], size = d["length"],
				crc = d["crc"], object_id = d["objectid"],
				download_url = d["download"]
			)
		return ret

	@staticmethod
	async def pan_file_info_res_id(
		file: dict = {"res_id": ""}, self = None
	):
		"""Get a file's information in the clouddisk
		with res_id anonymously.

		:param file: Resource ID in dictionary.
		:param self: ``Cldisk`` instance. Optional.
		:return: File information containing download state
		and the file.
		"""
		url = f"https://pan-yz.chaoxing.com/external/m/file/{file['res_id']}"
		headers = {
			**_Chaoxing_config_base["requests_headers"],
			"Referer": "https://pan-yz.chaoxing.com"
		}
		text = None
		if self:
			res = await self.get(url, headers = headers)
			if res.status == 200:
				text = await res.text()
		else:
			async with _request(
				"GET", url, headers = headers
			) as res:
				if res.status == 200:
					text = await res.text()
		ret = {**file, "result": False}
		if text:
			ret.update(await Cldisk.pan_file_info_object_id(file = {
				"object_id":
				_Cldisk_pan_file_info_res_id_regex.search(
					text
				)[1]
			}, self = self))
		return ret

	async def pan_file_info(
		self,
		file: dict = {"res_id": "", "object_id": "", "creator_uid": ""}
	):
		"""Get folder or file's information in the clouddisk.

		:param file: Resource ID and creator UID (optional,
		needed for other users' folder) or object ID (for files only).
		:return: File information containing name and resource ID.
		"""
		ret = {"name": "", "res_id": ""}
		if not file.get("res_id") and file.get("object_id"):
			ret.update(self.pan_file_info_object_id(
				file = file, self = self
			))
			return ret
		url = "https://pan-yz.chaoxing.com/pcNote/getFolderInfo"
		params = {
			"puid": file.get("creator_uid", self.__cx.uid),
			"parentId": file["res_id"]
		}
		res = await self.__cx.post(url, params = params)
		d = (await res.json(
			content_type = None
		)).get("data") if res.status == 200 else {}
		if d:
			ret.update(
				name = d["name"], type = d["resTypeValue"],
				size = d["size"], time_upload = _strftime(
					d["uploadDate"] // 1000
				) if "uploadDate" in d else "",
				time_modify = _strftime(
					d["modifyDate"] // 1000
				) if "modifyDate" in d else "",
				res_id = d["residstr"], crc = d.get("crc", ""),
				encrypted_id = d["encryptedId"],
				creator_uid = f"{d['creator']}"
			)
		return ret

	@staticmethod
	async def pan_file_upload_img(
		file: dict = {"file": None, "name": ".png"}, self = None
	):
		"""Upload image to the clouddisk anonymously.

		:param file: The image file and its name.
		The name extension must be correct.
		:param self: ``Cldisk`` instance. Optional.
		:return: File information containing object ID and download URL.
		Note that this object ID only works with this URL.
		"""
		url = "https://fanya.zyk2.chaoxing.com/upload/uploadImg"
		data = _FormData()
		data.add_field(
			"coverfile", file["file"], filename = file["name"]
		)
		ret = {**file, "result": False}
		d = None
		if self:
			res = await self.post(url, data = data)
			if res.status == 200:
				d = await res.json(content_type = None)
		else:
			async with _request("POST", url, data = data) as res:
				if res.status == 200:
					d = await res.json(content_type = None)
		if d and d["http"]:
			ret.update(
				object_id = d["objectId"],
				download_url = d["http"]
			)
		return ret

	async def pan_file_upload(
		self, file: dict = {"file": None, "name": ""},
		parent: dict = {"res_id": ""}
	):
		"""Upload file to the clouddisk.

		:param file: The file and its name (optional).
		:param parent: Resource ID of the parent folder. Optional.
		:return: File information containing upload state and object ID.
		"""
		url = (
			"https://pan-yz.chaoxing.com/upload"
			if parent.get("res_id") is None else
			"https://pan-yz.chaoxing.com/upload/uploadfile"
		)
		params = {
			"puid": self.__cx.uid,
			"_token": self.__secrets["clouddisk_token"],
			"fldid": parent.get("res_id", "")
		}
		data = _FormData()
		data.add_field("file", file["file"], filename = file.get(
			"name", f"cldisk-upload-{_trunc(_time() * 1000)}.txt"
		))
		res = await self.__cx.post(url, params = params, data = data)
		d = await res.json(content_type = None)
		ret = {
			"result": res.status == 200 and d.get("result"),
			"msg": d["msg"] if res.status == 200 else ""
		}
		if ret["result"]:
			d = d["data"]
			ret.update(
				result = True, name = d["name"],
				size = d["size"], time_upload = d["uploadDate"],
				time_modify = d["modifyDate"],
				object_id = d["objectId"],
				res_id = d["residstr"], crc = d["crc"],
				encrypted_id = d["encryptedId"],
				creator_uid = f"{d['creator']}"
			)
		return ret

	@staticmethod
	async def pan_file_download_res_id(
		file: dict = {"res_id": ""}, self = None
	):
		"""Download file from the clouddisk with res_id anonymously.

		:param file: Resource ID in dictionary.
		:param self: ``Cldisk`` instance. Optional.
		:return: File information containing download state
		and the file.
		"""
		url1 = f"https://pan-yz.chaoxing.com/external/m/file/{file['res_id']}"
		headers = {
			**_Chaoxing_config_base["requests_headers"],
			"Referer": "https://pan-yz.chaoxing.com"
		}
		text = None
		if self:
			res1 = await self.get(url1, headers = headers)
			if res1.status == 200:
				text = await res1.text()
		else:
			async with _request(
				"GET", url1, headers = headers
			) as res1:
				if res1.status == 200:
					text = await res1.text()
		ret = {**file, "result": False}
		if text:
			url2 = _Cldisk_pan_file_download_res_id_regex.search(
				text
			)[1]
			b = None
			if self:
				res2 = await self.get(
					url2, headers = headers
				)
				if res2.status == 200:
					b = await res2.read()
			else:
				async with _request(
					"GET", url2, headers = headers
				) as res2:
					if res2.status == 200:
						b = await res2.read()
			ret.update(file = _BytesIO(b), result = True)
		return ret

	async def pan_file_download(
		self, file: dict = {"res_id": "", "object_id": ""}
	):
		"""Download file from the clouddisk.

		:param file: Resource ID or object ID in dictionary.
		:return: File information containing download state
		and the file.
		"""
		if file.get("res_id"):
			return await self.pan_file_download_res_id(
				file = file, self = self
			)
		url1 = f"https://im.chaoxing.com/webim/file/status/{file['object_id']}"
		res1 = await self.__cx.get(url1, ttl = 1800)
		d = await res1.json()
		ret = {**file, "result": False}
		if not d["status"] if res1.status == 200 else False:
			url2 = d["download"]
			res2 = await self.__cx.get(url2, headers = {
				**_Chaoxing_config_base["requests_headers"],
				"Referer": "https://pan-yz.chaoxing.com"
			})
			if res2.status == 200:
				ret.update(file = _BytesIO(
					await res2.read()
				), result = True)
		return ret

	async def pan_file_move(
		self, file: dict = {"res_id": ""},
		parent: dict = {"res_id": ""}
	):
		"""Move file in the clouddisk.

		:param file: Resource ID in dictionary.
		:param parent: Resource ID of the destination folder.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/opt/moveres"
		data = {
			"folderid": f"""{parent.get(
				'res_id', ''
			)}_{self.__cx.uid}""", "resids": file["res_id"]
		}
		res = await self.__cx.post(url, data = data)
		return (await res.json(
			content_type = None
		))["success"] if res.status == 200 else False

	async def pan_file_rename(
		self, file = {"res_id": "", "name": ""},
	):
		"""Rename file in the clouddisk.

		:param file: Resource ID and its new name.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/opt/rename"
		data = {
			"puid": self.__cx.uid, "resid": file["resid"],
			"name": file["name"]
		}
		res = await self.__cx.post(url, data = data)
		return (await res.json(
			content_type = None
		))["success"] if res.status == 200 else False

	async def pan_file_delete(self, file: dict = {"res_id": ""}):
		"""Delete folder or file from the clouddisk.

		:param file: Resource ID in dictionary.
		:return: True on success.
		"""
		url = "https://pan-yz.chaoxing.com/api/delete"
		data = {
			"puid": self.__cx.uid, "resids": file["res_id"],
			"_token": self.__secrets["clouddisk_token"]
		}
		res = await self.__cx.post(url, data = data)
		return (await res.json(
			content_type = None
		))["data"][0]["success"] if res.status == 200 else False
