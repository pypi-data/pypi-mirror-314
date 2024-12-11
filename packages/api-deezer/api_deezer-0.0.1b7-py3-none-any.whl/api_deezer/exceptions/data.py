class Error_Data_404(Exception):
	def __init__(
		self,
		link: str,
		message: str = 'No Data info for \'{link}\''
	):
		self.link = link
		self.message = message

		super().__init__(
			self.message.format(
				link = link
			)
		)
