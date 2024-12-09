class Subtitles:
	def __init__(self, lang_code:str, lang_name:str, ext:str, url:str):
		self.code = lang_code
		self.name = lang_name
		self.extension = ext
		self.url = url

	def __str__(self): return f"Subtitles({self.code})"
	def __repr__(self): return str(self)


class SubtitlesManager:
	def __init__(self, subtitles_dict=None):
		self.subtitles = []
		self.raw_subtitles = subtitles_dict or {}
		for k, v in self.raw_subtitles.items():
			filtered = list(
				filter(
					lambda s: s.get('ext') == 'vtt' and s.get('protocol') != "m3u8_native"
				, v)
			)
			if len(filtered) > 0:
				sub = filtered[0]
				obj = Subtitles(
					lang_code=k.lower(),
					lang_name=sub.get('name'),
					ext=sub.get('ext'),
					url=sub.get('url')
				)
				self.subtitles.append(obj)

	def get(self, lang_code:str) -> Subtitles:
		'''Get subtitle by iso-code | returns Subtitles() or None'''
		code = str(lang_code.lower())
		return next((x for x in self.subtitles if x.code == code), None)


	def __str__(self): return f"Subtitles({len(self.subtitles)})"
	def __repr__(self): return str(self)
	def __len__(self): return len(self.subtitles)
	def __iter__(self): return iter(self.subtitles)
