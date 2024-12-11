from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from .contributor import Contributor

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Track_Album(BaseModel):
	id: int
	title: str
	link: str
	cover: str
	cover_small: str
	cover_medium: str
	cover_big: str
	cover_xl: str
	release_date: date


class Track_Artist(BaseModel):
	id: int
	name: str
	link: str
	share: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	radio: bool
	tracklist: str
	type: str


class Track(BaseModel):
	id: int
	readable: bool
	title: str
	title_short: str
	title_version: str | None = None
	#unseen: bool
	isrc: str
	link: str
	share: str
	duration: int
	track_position: int
	disk_number: int
	rank: int
	release_date: date
	explicit_lyrics: bool
	explicit_content_lyrics: Explicit_Content_Lyrics
	explicit_content_cover: Explicit_Content_Cover
	preview: str
	bpm: float
	gain: float
	available_countries: list[str]
	alternative: Track | None = None
	contributors: list[Contributor]
	md5_image: str
	artist: Track_Artist
	album: Track_Album
	type: str
