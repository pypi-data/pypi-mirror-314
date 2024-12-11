from datetime import date

from typing import Literal

from pydantic import (
	BaseModel, computed_field
)

from .image import Image
from .followers import Followers
from .linked_from import Linked_From
from .restrictions import Restrictions
from .external_urls import External_Urls


type ALBUM_TYPES = (
	Literal['album'] | Literal['single'] |
	Literal['compilation'] | Literal['ep']
)


class Short_User(BaseModel):
	external_urls: External_Urls
	followers: Followers | None = None
	href: str
	id: str
	type: Literal['user']
	uri: str


class Short_Artist(BaseModel):
	external_urls: External_Urls
	href: str
	id: str
	name: str
	type: Literal['artist']
	uri: str


class Short_Track(BaseModel):
	artists: list[Short_Artist]
	available_markets: list[str]
	disc_number: int
	duration_ms: int
	explicit: bool
	external_urls: External_Urls
	href: str
	id: str
	is_playable: bool = True
	linked_from: Linked_From | None = None
	restrictions: Restrictions | None = None
	name: str
	preview_url: str | None
	track_number: int
	type: Literal['track']
	uri: str
	is_local: bool


	@computed_field
	@property
	def duration(self) -> int:
		return self.duration_ms // 1000


class Short_Album(BaseModel):
	album_type: ALBUM_TYPES
	total_tracks: int
	available_markets: list[str]
	external_urls: External_Urls
	href: str
	id: str
	images: list[Image]
	name: str
	release_date: date | int
	release_date_precision: Literal['year'] | Literal['month'] | Literal['day']
	restrictions: Restrictions | None = None
	type: Literal['album']
	uri: str
	artists: list[Short_Artist]
