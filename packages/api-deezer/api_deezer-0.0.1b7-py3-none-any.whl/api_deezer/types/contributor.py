from pydantic import BaseModel


class Contributor(BaseModel):
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
	role: str
