from pydantic import BaseModel


class Genre(BaseModel):
	id: int
	name: str
	picture: str
	type: str
