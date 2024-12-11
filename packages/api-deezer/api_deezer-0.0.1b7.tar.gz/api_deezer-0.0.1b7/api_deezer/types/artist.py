from datetime import date

from pydantic import (
	BaseModel, Field
)

from .album import (
	Album_Track, Album_Track_Album, Album_Artist
)

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Artist(BaseModel):
	id: int
	name: str
	link: str
	share: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	nb_album: int
	nb_fan: int
	radio: bool
	tracklist: str
	type: str


class Artist_TOP(BaseModel):
	tracks: list[Album_Track] = Field(validation_alias = 'data')
	total: int


class Artist_Albums_Album(BaseModel):
	id: int
	title: str
	link: str
	cover: str
	cover_small: str
	cover_medium: str
	cover_big: str
	cover_xl: str
	md5_image: str
	genre_id: int
	release_date: date
	record_type: str
	tracklist: str
	explicit_lyrics: bool
	type: str


class Artist_Albums(BaseModel):
	albums: list[Artist_Albums_Album] = Field(validation_alias = 'data')
	total: int
	next: str | None = None


class Artist_Radio_Track(BaseModel):
	id: int
	readable: bool
	title: str
	title_short: str
	title_version: str | None = None
	duration: int
	rank: int
	explicit_lyrics: bool
	explicit_content_lyrics: Explicit_Content_Lyrics
	explicit_content_cover: Explicit_Content_Cover
	preview: str
	md5_image: str
	artist: Album_Artist
	album: Album_Track_Album
	type: str


class Artist_Radio(BaseModel):
	tracks: list[Artist_Radio_Track] = Field(validation_alias = 'data')


class Artist_Related_Artist(BaseModel):
	id: int
	name: str
	link: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	nb_album: int
	nb_fan: int
	radio: bool
	tracklist: str
	type: str


class Artist_Related(BaseModel):
	artists: list[Artist_Related_Artist] = Field(validation_alias = 'data')
	total: int
