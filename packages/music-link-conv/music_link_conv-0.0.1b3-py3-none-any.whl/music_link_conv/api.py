from api_deezer import API as API_Deezer
from api_deezer.exceptions.data import Error_Data_404 as Deezer_Error_Data_404

from api_spotify import API as API_Spotify


class Music_Link_Conv:
	def __init__(
		self,
		spotify_client_id: str,
		spotify_client_secret: str
	) -> None:

		self.__spotify_client_id = spotify_client_id
		self.__spotify_client_secret = spotify_client_secret
		self.__api_dee = API_Deezer()
		self.__api_spo = API_Spotify(self.__spotify_client_id, self.__spotify_client_secret)


	def conv_spo_track_2_dee_track(self, id_track: str) -> str | None:
		spotify_data = self.__api_spo.get_track(id_track)
		isrc = spotify_data.external_ids.isrc

		if not isrc:
			return

		try:
			deezer_data = self.__api_dee.get_track_by_isrc(isrc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link

	def conv_spo_album_2_dee_album(self, id_album: str) -> str | None:
		spotify_data = self.__api_spo.get_album(id_album)
		upc = spotify_data.external_ids.upc

		if not upc:
			return

		try:
			deezer_data = self.__api_dee.get_album_by_upc(upc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link

	def conv_spo_artist_2_dee_artist(self, id_artist: str) -> str | None:
		spotify_data = self.__api_spo.get_artist(id_artist)
		artist = spotify_data.name
		deezer_data = None

		if artist.find(" ") != -1:
			search = self.__api_dee.search(artist)

			for found in search.results:
				if found.artist.name == artist:
					deezer_data = found.artist
					break
		else:
			try:
				deezer_data = self.__api_dee.get_artist(artist)
			except Deezer_Error_Data_404:
				return

		if not deezer_data:
			return

		return deezer_data.link
