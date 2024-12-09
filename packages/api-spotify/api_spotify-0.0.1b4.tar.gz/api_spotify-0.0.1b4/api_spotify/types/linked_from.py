from typing import Literal

from pydantic import BaseModel

from .external_urls import External_Urls


class Linked_From(BaseModel):
	external_urls: External_Urls
	href: str
	id: str
	type: Literal['track']
	uri: str
