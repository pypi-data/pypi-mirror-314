from typing import Any

from logging import getLogger

from requests import Session
from requests import post as req_post

from json import dump as JSON_dump

from .decorators import check_login

from .types import (
	Token, Album, Album_Tracks,
	New_Releases, Track,
	Playlist, Artist
)


class API:
	API_URL = 'https://api.spotify.com/v1/'
	logger = getLogger('API_SPOTIFY')
	API_ACCESS_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token' # trunk-ignore(bandit/B105)


	def __init__(self, client_id: str, client_secret: str) -> None:
		self.__client_id = client_id
		self.__client_secret = client_secret
		self.__session = Session()
		self.refresh()


	def write_log(
		self,
		json: dict[str, Any], 
		path: str = 'out.json'
	) -> None:

		with open(path, 'w') as f:
			JSON_dump(json, f)


	def refresh(self) -> None:
		params = {
			'grant_type': 'client_credentials',
			'client_id': self.__client_id,
			'client_secret': self.__client_secret
		}

		json_data = req_post(
			self.API_ACCESS_TOKEN_ENDPOINT,
			data = params,
			timeout = 30
		).json()

		self.token = Token.model_validate(json_data)
		self.__session.headers['Authorization'] = f'Bearer {self.token.access_token}'


	@check_login
	def make_req(self, method: str) -> dict[str, Any]:
		return self.__session.get(f'{self.API_URL}{method}').json()


	def get_track_JSON(self, id_track: str) -> dict[str, Any]:
		method = f'tracks/{id_track}'
		self.write_log(self.make_req(method))

		return self.make_req(method)


	def get_track(self, id_track: str) -> Track:
		res = self.get_track_JSON(id_track)

		return Track.model_validate(res)


	def get_album_JSON(self, id_album: str) -> dict[str, Any]:
		method = f'albums/{id_album}'

		return self.make_req(method)


	def get_album(self, id_album: str) -> Album:
		res = self.get_album_JSON(id_album)
		res['tracks']['_api'] = self

		return Album.model_validate(res)
	

	def get_album_tracks_JSON(self, id_album: str) -> dict[str, Any]:
		method = f'albums/{id_album}/tracks'

		return self.make_req(method)


	def get_album_tracks(self, id_album: str) -> Album_Tracks:
		res = self.get_album_tracks_JSON(id_album)
		res['_api'] = self

		return Album_Tracks.model_validate(res)


	def get_new_releases_JSON(self) -> dict[str, Any]:
		method = 'browse/new-releases'

		return self.make_req(method)


	def get_new_releases(self) -> New_Releases:
		res = self.get_new_releases_JSON()
		res['albums']['_api'] = self

		return New_Releases.model_validate(res)


	def get_playlist_JSON(self, id_playlist: str) -> dict[str, Any]:
		method = f'playlists/{id_playlist}'

		return self.make_req(method)


	def get_playlist(self, id_playlist: str) -> Playlist:
		res = self.get_playlist_JSON(id_playlist)
		res['tracks']['_api'] = self

		return Playlist.model_validate(res)


	def get_artist_JSON(self, id_artist: str) -> dict[str, Any]:
		method = f'artists/{id_artist}'

		return self.make_req(method)


	def get_artist(self, id_artist: str) -> Artist:
		res = self.get_artist_JSON(id_artist)

		return Artist.model_validate(res)
