from .youtube import YouTube
from .utils import Thumbnail, Channel


class PlaylistVideo:
	'''Lazy load video'''
	def __init__(self, title:str, link:str, duration:int, channel:Channel, thumbnail:Thumbnail, cookies:list=None):
		self.yt_obj = None
		self.cookies = cookies
		self.link = link
		self.title = title
		self.duration = duration
		self.thumbnail = thumbnail
		self.channel = channel
		self.author = channel.name

	def load(self) -> YouTube:
		if not self.yt_obj:
			self.yt_obj = YouTube(self.link, cookies=self.cookies)
		return self.yt_obj

	def __str__(self): return f"PlaylistVideo({self.link})"
	def __repr__(self): return str(self)

class DeletedVideo:
	def __init__(self, link):
		self.link = link
	def __bool__(self): return False
	def load(self): return self


class PlaylistManager:
	def __init__(self, array=None):
		self.arr = array or []
		self.index = 0
	def __len__(self): return len(self.arr)
	def __getitem__(self, key):
		if isinstance(key, slice):
			return (self.arr[i].load() for i in range(*key.indices(len(self.arr))))
		elif isinstance(key, int):
			return self.arr[key].load()
		raise TypeError("Invalid argument type")

	def __iter__(self):
		self.index = 0
		self.end = len(self.arr)
		return self
	def __next__(self) -> YouTube:
		if self.index >= self.end: raise StopIteration
		item = self.arr[self.index]
		self.index += 1
		return item.load()
