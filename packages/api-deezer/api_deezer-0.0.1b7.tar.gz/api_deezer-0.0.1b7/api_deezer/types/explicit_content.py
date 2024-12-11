from pydantic import (
	BaseModel, model_validator
)


types_explicit_content_lyrics = {
	0: 'Not Explicit',
	1: 'Explicit',
	2: 'Unknown',
	3: 'Edited',
	4: 'Partially Explicit (Album "lyrics" only)',
	5: 'Partially Unknown (Album "lyrics" only)',
	6: 'No Advice Available',
	7: 'Partially No Advice Available (Album "lyrics" only)'
}


types_explicit_content_cover = {
	0: 'Not Explicit',
	1: 'Explicit',
	2: 'Unknown',
	6: 'No Advice Available',
}


class Explicit_Content_Lyrics(BaseModel):
	id: int
	mean: str


	@model_validator(mode = 'before')
	@classmethod
	def make_explicit_content_lyrics(cls, iecl: int) -> dict[str, int | str]:
		return {
			'id': iecl,
			'mean':  types_explicit_content_lyrics[iecl]
		}


class Explicit_Content_Cover(BaseModel):
	id: int
	mean: str


	@model_validator(mode = 'before')
	@classmethod
	def make_explicit_content_cover(cls, iecc: int) -> dict[str, int | str]:
		return {
			'id': iecc,
			'mean':  types_explicit_content_lyrics[iecc]
		}
