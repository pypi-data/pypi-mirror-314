from pydantic import BaseModel


class External_Ids(BaseModel):
	isrc: str | None = None
	ean: str | None = None
	upc: str | None = None
