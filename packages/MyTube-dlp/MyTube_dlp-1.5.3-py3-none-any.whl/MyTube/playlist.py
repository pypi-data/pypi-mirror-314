import os
import yt_dlp
import tempfile
from .playlist_manager import PlaylistManager, PlaylistVideo, DeletedVideo
from .utils import Thumbnail, Channel
from .utils import get_cookie_file


class Playlist:
	def __init__(self, link, cookies:list=None):
		self.link = link
		self._info = None
		self._videos = []
		self.cookies = cookies
		cookie_file = get_cookie_file(cookies) if cookies else None

		ydl_opts = {
			'quiet': True,
			'extract_flat': True,
			'skip_download': True,
			"cookiefile": cookie_file
		}
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			self._info = ydl.extract_info(link, download=False)

		if cookie_file and os.path.exists(cookie_file): os.remove(cookie_file)
		if self._info.get('_type') != 'playlist': raise TypeError(f"[Not playlist]: {link}")

		for item in self._info.get('entries'):
			if not item.get('duration'):
				self._videos.append(DeletedVideo(link=item.get('url')))
			else:
				best_image = max(item.get('thumbnails'), key=lambda img: img['width']*img['height'])
				channel = Channel(
					id=item.get('channel_id'),
					url=item.get('channel_url'),
					name=item.get('channel')
				)
				self._videos.append(
					PlaylistVideo(
						title=item.get('title'),
						link=item.get('url'),
						duration=int(item.get('duration')),
						channel=channel,
						thumbnail=Thumbnail(best_image.get('url')),
						cookies=self.cookies
					)
				)

	@property
	def playlistId(self) -> str:
		return str(self._info.get('id'))
	@property
	def title(self) -> str:
		return str(self._info.get('title'))
	@property
	def description(self) -> str:
		return str(self._info.get('description'))
	
	@property
	def type(self):
		'''"private" or "public"'''
		return "private" if self._info.get('availability') == "private" else "public"

	@property
	def videos(self) -> PlaylistManager:
		return PlaylistManager([v for v in self._videos if isinstance(v, PlaylistVideo)])
	@property
	def raw_videos(self) -> list: return self._videos

	def __str__(self): return f"Playlist(«{self.title}»)"
	def __repr__(self): return str(self)
