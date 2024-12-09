from __future__ import annotations

from typing import (
	Any, TYPE_CHECKING
)

from pydantic import (
	BaseModel, model_validator
)

from .shorts import Short_Album


if TYPE_CHECKING:
	from ..api import API


class New_Releases_Albums(BaseModel):
	href: str
	limit: int
	offset: int
	next: str | None
	previous: str | None
	total: int
	items: list[Short_Album]


	@model_validator(mode = 'before')
	@classmethod
	def check(cls, data: dict[str, Any]) -> dict[str, Any]:
		cls.__api: API = data['_api']

		return data


	def get_next(self) -> New_Releases_Albums | None:
		if not self.next:
			return

		method = self.next.removeprefix(self.__api.API_URL)
		res = self.__api.make_req(method)
		res['_api'] = self.__api

		return New_Releases_Albums.model_validate(res)


class New_Releases(BaseModel):
	albums: New_Releases_Albums
