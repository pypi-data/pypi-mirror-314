from pydantic import (
	BaseModel, Field
)

from .explicit_content import (
	Explicit_Content_Lyrics, Explicit_Content_Cover
)


class Result_Artist(BaseModel):
	id: int
	name: str
	link: str
	picture: str
	picture_small: str
	picture_medium: str
	picture_big: str
	picture_xl: str
	tracklist: str
	type: str


class Result_Album(BaseModel):
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


class Result(BaseModel):
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
	artist: Result_Artist
	album: Result_Album
	type: str


class Search(BaseModel):
	results: list[Result] = Field(validation_alias = 'data')
