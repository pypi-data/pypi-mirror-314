__all__ = ("locations", )

from ast import literal_eval as _literal_eval
from os.path import join as _join
from pkgutil import get_data as _get_data

_locations_str = _get_data(
	"xdcheckin.server", _join("static", "g_locations.js")
).decode("utf-8")

locations = _literal_eval(_locations_str[
	_locations_str.index("{") : _locations_str.rindex("}") + 1
])
