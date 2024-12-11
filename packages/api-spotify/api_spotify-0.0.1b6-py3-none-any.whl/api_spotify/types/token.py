from datetime import datetime

from pydantic import (
	BaseModel, computed_field
)


class Token(BaseModel):
	access_token: str
	token_type: str
	expires_in: int


	@computed_field
	@property
	def created_at(self) -> datetime:
		return datetime.now()
