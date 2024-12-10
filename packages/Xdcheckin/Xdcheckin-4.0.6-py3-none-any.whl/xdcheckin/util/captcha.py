__all__ = (
	"chaoxing_captcha_get_checksum", "solve_captcha_rotate",
	"solve_captcha_slide"
)

from hashlib import md5 as _md5
from math import cos as _cos, sin as _sin, radians as _radians, trunc as _trunc
from time import time as _time
from uuid import uuid4 as _uuid4

def chaoxing_captcha_get_checksum(
	captcha: dict = {"captcha_id": "", "server_time": "", "type": ""}
):
	"""Generate key and token for CAPTCHA images.

 	:param: CAPTCHA ID, server timestamp and CAPTCHA type.
  	:return: CAPTCHA key and token.
 	"""
	id = captcha["captcha_id"]
	time = captcha["server_time"]
	type = captcha["type"]
	key = _md5(f"{time}{_uuid4()}".encode("utf-8")).hexdigest()
	token = f"""{_md5(
		f"{time}{id}{type}{key}".encode("utf-8")
	).hexdigest()}:{int(time) + 300000}"""
	iv = _md5(
		f"{id}{type}{_trunc(_time() * 1000)}{_uuid4()}".encode("utf-8")
	).hexdigest()
	return key, token, iv

def solve_captcha_rotate(big_img = None, small_img = None, radius: int = 157):
	width_b = big_img.width
	width_s = small_img.width
	xc_t = big_img.width // 2
	yc_t = big_img.height // 2
	xc_w = small_img.width // 2
	yc_w = small_img.height // 2
	height_t = 1
	len_t = height_t * 360
	radius_w = radius - height_t
	plt_b = big_img.getpalette()
	plt_s = small_img.getpalette()
	trigs = []
	for x in range(360):
		rad = _radians(x)
		trigs.append((_cos(rad), _sin(rad)))
	template = [0] * (height_t * 360)
	window = template.copy()
	sum_t = sum_w = 0
	for x, (cos_r, sin_r) in enumerate(trigs):
		i = x
		r_t = radius
		r_w = radius_w
		for _ in range(height_t):
			p_t = big_img.im[
				(_trunc(r_t * sin_r) + yc_t) * width_b +
				_trunc(r_t * cos_r) + xc_t
			] * 3
			t = plt_b[p_t] + plt_b[p_t + 1] + plt_b[p_t + 2]
			template[i] = t
			sum_t += t
			p_w = small_img.im[
				(_trunc(r_w * sin_r) + yc_w) * width_s +
				_trunc(r_w * cos_r) + xc_w
			] * 3
			w = plt_s[p_w] + plt_s[p_w + 1] + plt_s[p_w + 2]
			window[i] = w
			sum_w += w
			r_t += 1
			r_w += 1
			i += 360
	mean_t = sum_t / len_t
	mean_w = sum_w / len_t
	for i in range(len_t):
		template[i] -= mean_t
		window[i] -= mean_w
	ncc_max = d_max = 0
	for d in range(9, 360, 9):
		ncc = 0
		for i, t in enumerate(template):
			x = i % 360
			ncc += window[i - x + (x - d) % 360] * t
		if ncc > ncc_max:
			ncc_max = ncc
			d_max = d
	return d_max

def solve_captcha_slide(big_img = None, small_img = None, border: int = 8):
	"""Slider CAPTCHA solver based on normalized cross-correlation.

	:param big_img: Background image with slider piece embedded.
	:param small_img: Slider image vertically aligned with
	transparent padding.
	:param border: Border width of the slider piece.
	8 by default for Chaoxing's and 24 recommended for IDS's.
	:return: Slider offset.
	"""
	big_img.load()
	small_img.load()
	x_l, y_t, x_r, y_b = small_img.im.getband(3).point((
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
	), None).getbbox()
	x_l += border
	y_t += border
	x_r -= border
	y_b -= border
	template = small_img.im.crop((x_l, y_t, x_r, y_b)).convert("L", 3)
	width_w = x_r - x_l
	len_w = width_w * (y_b - y_t)
	mean_t = sum(template) / len_w
	template = [v - mean_t for v in template]
	width_g = big_img.width - small_img.width + width_w - 1
	grayscale = big_img.im.convert("L", 3)
	cols_w = [
		sum(grayscale[y * big_img.width + x] for y in range(y_t, y_b))
		for x in range(x_l + 1, width_g + 1)
	]
	cols_w_l = iter(cols_w)
	cols_w_r = iter(cols_w)
	sum_w = sum(next(cols_w_r) for _ in range(width_w))
	ncc_max = x_max = 0
	for x in range(x_l + 1, width_g - width_w, 2):
		sum_w = (
			sum_w - next(cols_w_l) - next(cols_w_l) +
			next(cols_w_r) + next(cols_w_r)
		)
		mean_w = sum_w / len_w
		ncc = 0
		sum_ww = 0.000001
		for w, t in zip(grayscale.crop((
			x, y_t, x + width_w, y_b
		)), template):
			w -= mean_w
			ncc += w * t
			sum_ww += w * w
		ncc /= sum_ww
		if ncc > ncc_max:
			ncc_max = ncc
			x_max = x
	return x_max - x_l - 1
