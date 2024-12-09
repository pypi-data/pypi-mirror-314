from enum import StrEnum

from urllib.parse import urlparse
from requests import get as req_get

from .exceptions import Invalid_Link


VALID_DOMAINS = (
	'spotify.com', 'open.spotify.com'
)

NOT_VERIFY = VALID_DOMAINS[1:]


class Type_Media(StrEnum):
	TRACK = 'track'
	ALBUM = 'album'
	PLAYLIST = 'playlist'
	#ARTIST = 'artist'


types_media = {
	type_media.value: type_media
	for type_media in Type_Media
}


def magic_link(link: str) -> tuple[Type_Media, str]:
	url_parsed = urlparse(link)

	if url_parsed.netloc in VALID_DOMAINS:
		path = url_parsed.path
	else:
		raise Invalid_Link(link)

	res = req_get(
		link,
		timeout = 60
	)

	if res.status_code == 404:
		raise Invalid_Link(link)

	s_path = path.split('/')
	id_media = s_path[-1]
	type_media = s_path[-2]

	return types_media[type_media], id_media
