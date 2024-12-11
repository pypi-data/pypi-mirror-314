from pydantic import BaseModel


class Image(BaseModel):
	url: str
	height: int | None
	width: int | None
