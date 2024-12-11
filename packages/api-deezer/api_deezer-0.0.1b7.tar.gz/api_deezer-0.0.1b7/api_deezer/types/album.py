from __future__ import annotations

from datetime import date

from typing import Annotated

from pydantic import (
	BaseModel, BeforeValidator
)

from .genre import Genre
from .contributor import Contributor

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Album_Artist(BaseModel):
	id: int
	name: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	tracklist: str
	type: str


class Album_Track_Artist(BaseModel):
	id: int
	name: str
	tracklist: str
	type: str


class Album_Track_Album(BaseModel):
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


class Album_Track(BaseModel):
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
	preview: str
	md5_image: str
	artist: Album_Track_Artist
	album: Album_Track_Album
	type: str


Album_Tracks = Annotated[
	list[Album_Track], BeforeValidator(
		lambda tracks: tracks['data']
	)
]


type Genres = Annotated[
	list[Genre], BeforeValidator(
		lambda data: data['data']
	)
]


class Album(BaseModel):
	id: int
	title: str
	upc: str
	link: str
	share: str
	cover: str
	cover_small: str
	cover_medium: str
	cover_big: str
	cover_xl: str
	md5_image: str
	genre_id: int
	genres: Genres
	nb_tracks: int
	duration: int
	fans: int
	release_date: date
	record_type: str
	available: bool
	alternative: Album | None = None
	tracklist: str
	explicit_lyrics: bool
	explicit_content_lyrics: Explicit_Content_Lyrics
	explicit_content_cover: Explicit_Content_Cover
	contributors: list[Contributor]
	artist: Album_Artist
	type: str
	tracks: Album_Tracks
