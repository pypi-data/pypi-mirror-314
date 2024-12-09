from .artist import Artist
from .external_ids import External_Ids

from .shorts import (
	Short_Track, Short_Album
)


class Track(Short_Track):
	album: Short_Album
	artists: list[Artist] #pyright: ignore [reportIncompatibleVariableOverride]
	external_ids: External_Ids
	popularity: int
