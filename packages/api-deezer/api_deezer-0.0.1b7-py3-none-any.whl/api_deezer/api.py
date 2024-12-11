from typing import Any

from requests import get as req_get

from .types import (
	Track, Album,
	Playlist, Artist, Search,
	Artist_TOP, Artist_Albums,
	Artist_Radio, Artist_Related, Chart
)

from .exceptions.data import Error_Data_404


class API:
	__API_URL = 'https://api.deezer.com/'


	def __make_req(self, endpoint: str):
		c_api_url = f'{self.__API_URL}{endpoint}'
		json_data: dict[str, Any] = req_get(c_api_url).json()
		is_error: dict[str, Any] | None = json_data.get('error')

		if is_error:
			match is_error['type']:
				case 'DataException':
					raise Error_Data_404(endpoint)
				case _:
					raise Exception(f'Error {is_error['type']} unknown. Link {c_api_url}. Report this kindly :)')

		return json_data


	def get_track_JSON(self, id_track: int | str) -> dict[str, Any]:
		"""

		Function for getting Track's infos in JSON format

		"""

		endpoint = f'/track/{id_track}'

		return self.__make_req(endpoint)


	def get_track_by_isrc_JSON(self, isrc: str) -> dict[str, Any]:
		"""

		Function for getting Track's infos in JSON format by ISRC

		"""

		endpoint = f'/track/isrc:{isrc}'

		return self.__make_req(endpoint)


	def get_track_by_isrc(self, isrc: str) -> Track:
		res = self.get_track_by_isrc_JSON(isrc)

		return Track.model_validate(res)


	def get_track(self, id_track: int | str) -> Track:
		res = self.get_track_JSON(id_track)

		return Track.model_validate(res)  # https://docs.pydantic.dev/latest/concepts/models/#helper-functions


	def get_album_JSON(self, id_album: int | str) -> dict[str, Any]:
		"""

		Function for getting Album's infos in JSON format

		"""

		endpoint = f'/album/{id_album}'

		return self.__make_req(endpoint)


	def get_album_by_upc_JSON(self, upc:  int | str) -> dict[str, Any]:
		"""

		Function for getting Album's infos in JSON format by UPC

		"""

		endpoint = f'/album/upc:{upc}'

		return self.__make_req(endpoint)


	def get_album_by_upc(self, upc: int | str) -> Album:
		res = self.get_album_by_upc_JSON(upc)

		return Album.model_validate(res)


	def get_album(self, id_album: int | str) -> Album:
		res = self.get_album_JSON(id_album)

		return Album.model_validate(res)


	def get_artist_JSON(self, id_artist: int | str) -> dict[str, Any]:
		"""

		Function for getting Artist's infos in JSON format

		"""

		endpoint = f'/artist/{id_artist}'

		return self.__make_req(endpoint)


	def get_artist(self, id_artist: int | str) -> Artist:
		res = self.get_artist_JSON(id_artist)

		return Artist.model_validate(res)


	def get_artist_top_JSON(self, id_artist: int | str, limit: int = 50) -> dict[str, Any]:
		"""

		Function for getting Artist's top infos in JSON format

		"""

		endpoint = f'/artist/{id_artist}/top?limit={limit}'

		return self.__make_req(endpoint)


	def get_artist_top(self, id_artist: int | str, limit: int = 50) -> Artist_TOP:
		res = self.get_artist_top_JSON(id_artist, limit)

		return Artist_TOP.model_validate(res)


	def get_artist_radio_JSON(self, id_artist: int | str) -> dict[str, Any]:
		"""

		Function for getting Artist's radio infos in JSON format

		"""

		endpoint = f'/artist/{id_artist}/radio'

		return self.__make_req(endpoint)


	def get_artist_radio(self, id_artist: int | str) -> Artist_Radio:
		res = self.get_artist_radio_JSON(id_artist)

		return Artist_Radio.model_validate(res)


	def get_artist_related_JSON(self, id_artist: int | str) -> dict[str, Any]:
		"""

		Function for getting Artist's radio infos in JSON format

		"""

		endpoint = f'/artist/{id_artist}/related'

		return self.__make_req(endpoint)


	def get_artist_related(self, id_artist: int | str) -> Artist_Related:
		res = self.get_artist_related_JSON(id_artist)

		return Artist_Related.model_validate(res)


	def get_artist_albums_JSON(self, id_artist: int | str, limit: int = 50) -> dict[str, Any]:
		"""

		Function for getting Artist's albums infos in JSON format

		"""

		endpoint = f'/artist/{id_artist}/albums?limit={limit}'

		return self.__make_req(endpoint)


	def get_artist_albums(self, id_artist: int | str, limit: int = 50) -> Artist_Albums:
		res = self.get_artist_albums_JSON(id_artist, limit)

		return Artist_Albums.model_validate(res)


	def get_playlist_JSON(self, id_playlist: int | str) -> dict[str, Any]:
		"""

		Function for getting Playlist's infos in JSON format

		"""

		endpoint = f'/playlist/{id_playlist}'

		return self.__make_req(endpoint)


	def get_playlist(self, id_playlist: int | str) -> Playlist:
		res = self.get_playlist_JSON(id_playlist)

		return Playlist.model_validate(res)


	def get_chart_JSON(self) -> dict[str, Any]:
		"""

		Function for getting Chart's infos in JSON format

		"""

		endpoint = '/chart'

		return self.__make_req(endpoint)


	def get_chart(self) -> Chart:
		res = self.get_chart_JSON()

		return Chart.model_validate(res)


	def search_JSON(self, q: str) -> dict[str, Any]:
		method = 'search'
		url = f'{self.__API_URL}{method}?q={q}'
		res = req_get(url).json()

		return res


	def search(self, q: str) -> Search:
		res = self.search_JSON(q)

		return Search.model_validate(res)
