from __future__ import annotations

from datetime import datetime

from typing import (
	Any, TYPE_CHECKING, Literal
)

from pydantic import (
	BaseModel, model_validator
)

from .image import Image
from .owner import Owner
from .track import Track
from .shorts import Short_User
from .followers import Followers
from .external_urls import External_Urls


if TYPE_CHECKING:
	from ..api import API


class Playlist_Tracks_Item(BaseModel):
	added_at: datetime
	added_by: Short_User
	is_local: bool
	track: Track


class Playlist_Tracks(BaseModel):
	href: str
	limit: int
	offset: int
	next: str | None
	previous: str | None
	total: int
	items: list[Playlist_Tracks_Item]


	@model_validator(mode = 'before')
	@classmethod
	def check(cls, data: dict[str, Any]) -> dict[str, Any]:
		cls.__api: API = data['_api']

		return data


	def __get(self, endpoint: str | None) -> Playlist_Tracks | None:
		if not endpoint:
			return

		method = endpoint.removeprefix(self.__api.API_URL)
		res = self.__api.make_req(method)
		res['_api'] = self.__api

		return Playlist_Tracks.model_validate(res)


	def get_next(self) -> Playlist_Tracks | None:
		return self.__get(self.next)


	def get_previous(self) -> Playlist_Tracks | None:
		return self.__get(self.previous)


class Playlist(BaseModel):
	collaborative: bool
	description: str | None
	external_urls: External_Urls
	followers: Followers
	href: str
	id: str
	images: list[Image]
	name: str
	owner: Owner
	public: bool
	snapshot_id: str
	tracks: Playlist_Tracks
	type: Literal['playlist']
	uri: str
