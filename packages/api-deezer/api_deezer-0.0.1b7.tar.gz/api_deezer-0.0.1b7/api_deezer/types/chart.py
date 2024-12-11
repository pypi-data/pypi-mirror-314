from pydantic import BaseModel

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Chart_Media_Artist(BaseModel):
	id: int
	name: str
	link: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	radio: bool
	tracklist: str
	type: str


class Chart_Track_Album(BaseModel):
	id: int
	title: str
	cover: str
	cover_small: str
	cover_medium: str
	cover_big: str
	cover_xl: str
	md5_image: str
	tracklist: str
	type: str


class Chart_Track(BaseModel):
	id: int
	title: str
	title_short: str
	title_version: str
	link: str
	duration: int
	rank: int
	explicit_lyrics: bool
	explicit_content_lyrics: Explicit_Content_Lyrics
	explicit_content_cover: Explicit_Content_Cover
	preview: str
	md5_image: str
	position: int
	artist: Chart_Media_Artist
	album: Chart_Track_Album
	type: str


class Chart_Tracks(BaseModel):
	data: list[Chart_Track]
	total: int


class Chart_Album(BaseModel):
	id: int
	title: str
	link: str
	cover: str
	cover_small: str
	cover_medium: str
	cover_big: str
	cover_xl: str
	md5_image: str
	record_type: str
	tracklist: str
	explicit_lyrics: bool
	position: int
	artist: Chart_Media_Artist
	type: str


class Chart_Albums(BaseModel):
	data: list[Chart_Album]
	total: int


class Chart_Artist(BaseModel):
	id: int
	name: str
	link: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	radio: bool
	tracklist: str
	position: int
	type: str


class Chart_Artists(BaseModel):
	data: list[Chart_Artist]
	total: int


class User(BaseModel):
	id: int
	name: str
	tracklist: str
	type: str


class Chart_Playlist(BaseModel):
	id: int
	title: str
	public: bool
	nb_tracks: int
	link: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	checksum: str
	tracklist: str
	creation_date: str
	md5_image: str
	picture_type: str
	user: User
	type: str


class Chart_Playlists(BaseModel):
	data: list[Chart_Playlist]
	total: int


class Chart_Podcast(BaseModel):
	id: int
	title: str
	description: str
	available: bool
	fans: int
	link: str
	share: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	type: str


class Chart_Podcasts(BaseModel):
	data: list[Chart_Podcast]
	total: int


class Chart(BaseModel):
	tracks: Chart_Tracks
	albums: Chart_Albums
	artists: Chart_Artists
	playlists: Chart_Playlists
	podcasts: Chart_Podcasts
