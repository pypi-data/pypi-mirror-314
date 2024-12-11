from typing import Annotated

from datetime import datetime

from pydantic import (
	BaseModel, BeforeValidator
)

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Playlist_Creator(BaseModel):
	id: int
	name: str
	tracklist: str
	type: str


class Playlist_Track_Artist(BaseModel):
	id: int
	name: str
	link: str
	tracklist: str
	type: str


class Playlist_Track_Album(BaseModel):
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


class Playlist_Track(BaseModel):
	id: int
	readable: bool
	title: str
	title_short: str
	title_version: str | None = None
	link: str
	duration: int
	rank: int
	explicit_lyrics: bool
	explicit_content_lyrics: Explicit_Content_Lyrics
	explicit_content_cover: Explicit_Content_Cover
	preview: str | None = None
	md5_image: str
	time_add: int
	artist: Playlist_Track_Artist
	album: Playlist_Track_Album
	type: str


Playlist_Tracks = Annotated[
	list[Playlist_Track], BeforeValidator(
		lambda tracks: tracks['data']
	)
]


class Playlist(BaseModel):
	id: int
	title: str
	description: str
	duration: int
	public: bool
	is_loved_track: bool
	collaborative: bool
	nb_tracks: int
	fans: int
	link: str
	share: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	checksum: str
	creation_date: datetime
	md5_image: str
	picture_type: str
	creator: Playlist_Creator
	type: str
	tracks: Playlist_Tracks
