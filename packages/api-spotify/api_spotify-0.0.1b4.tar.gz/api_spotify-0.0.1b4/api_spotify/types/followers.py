from pydantic import BaseModel


class Followers(BaseModel):
	href: str | None
	total: int
