from .utils import get_file_path
from .downloader import Downloader


class Stream:
	def __init__(self, itag:str, url:str, filesize:int, metadata:dict=None):
		self.itag = itag
		self.url = url
		self.filesize = filesize
		self.metadata = metadata or {}
		self.isVideo = False
		self.isAudio = False
		self.isMuxed = False

	def get(self, attribute_name, default=0):
		return getattr(self, attribute_name, default)

	@property
	def w(self): return self.width
	@property
	def h(self): return self.height
	@property
	def res(self): return min(self.height, self.width)
	@property
	def lang(self): return self.language
	@property
	def abr(self): return self.audioBitrate
	@property
	def asr(self): return self.audioSamplerate
	
	def add_video_info(self,
		videoCodec:str,
		videoExt:str,
		width:int,
		height:int,
		fps:int
	):
		self.videoCodec = videoCodec
		self.videoExt = videoExt
		self.width = width
		self.height = height
		self.fps = fps
		self.isVideo = True

	def add_audio_info(self,
		audioCodec:str,
		audioExt:str,
		language:str,
		audioBitrate:int,
		audioSamplerate:int
	):
		self.audioCodec = audioCodec
		self.audioExt = audioExt
		self.language = language
		self.audioBitrate = audioBitrate
		self.audioSamplerate = audioSamplerate
		self.isAudio = True

	def add_muxed_info(self,
		videoCodec:str,
		videoExt:str,
		width:int,
		height:int,
		fps:int,
		audioCodec:str,
		language:str,
		audioSamplerate:int
	):
		self.videoCodec = videoCodec
		self.videoExt = videoExt
		self.width = width
		self.height = height
		self.fps = fps
		self.audioCodec = audioCodec
		self.language = language
		self.audioSamplerate = audioSamplerate
		self.isMuxed = True

	def __str__(self):
		if self.isVideo:
			return f"Video({self.width}x{self.height}.{self.videoExt} [{self.fps}fps] {self.videoCodec})"
		elif self.isAudio:
			return f"Audio({self.audioBitrate}.{self.audioExt}{' ['+self.language+']' if self.language else ''} {self.audioCodec})"
		elif self.isMuxed:
			return f"Muxed({self.width}x{self.height}.{self.videoExt} [{self.fps}fps]{' ['+self.language+']' if self.language else ''} {self.videoCodec}+{self.audioCodec})"
		else:
			return f"Stream(id={self.itag})"

	def __repr__(self):
		if self.isVideo:
			return f"Video({self.res}p)"
		elif self.isAudio:
			return f"Audio({self.audioBitrate}kbps)"
		elif self.isMuxed:
			return f"Muxed({self.res}p)"
		else:
			return f"Stream({self.itag})"


	async def download(self, *args, **kwargs) -> str:
		if self.isVideo or self.isMuxed:
			dwnl = Downloader(video=self, metadata=self.metadata)
		else:
			dwnl = Downloader(audio=self, metadata=self.metadata)
		return await dwnl(*args, **kwargs)
	