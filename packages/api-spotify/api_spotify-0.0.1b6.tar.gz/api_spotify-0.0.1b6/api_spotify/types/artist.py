from .image import Image
from .followers import Followers
from .shorts import Short_Artist


class Artist(Short_Artist):
	followers: Followers | None = None
	genres: list[str] | None = None
	images: list[Image] | None = None
	popularity: int | None = None
