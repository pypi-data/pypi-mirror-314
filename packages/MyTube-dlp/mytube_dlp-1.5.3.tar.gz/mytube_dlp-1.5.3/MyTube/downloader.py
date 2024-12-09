import os
import re
import aiohttp
import tempfile
import subprocess
from .utils import get_file_path, to_seconds


class Downloader:
	def __init__(self, video:"Stream"=None, audio:"Stream"=None, metadata:dict=None):
		self.videoStream = video if (video and (video.isVideo or video.isMuxed)) else None
		self.audioStream = audio if (audio and audio.isAudio) else None
		self.metadata = metadata or {}
		self.can_download = True
		self.CHUNK_SIZE = 10*1024*1024
		self.HEADERS = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
			"Accept-Language": "en-US,en"
		}
		self.FFMPEG = "ffmpeg"
		self._DURATION_REG = re.compile(
			r"Duration: (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"
		)
		self._TIME_REG = re.compile(
			r"time=(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})"
		)
		self.startupinfo = None
		if os.name == 'nt':
			self.startupinfo = subprocess.STARTUPINFO()
			self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

	async def _default_progress(self, current, total): return

	def abort(self):
		self.can_download = False

	def reserve_file(self, file):
		with open(file, 'w') as f:
			f.write("0")

	def remove_file(self, file):
		if os.path.exists(file): os.remove(file)

	async def __call__(self,
		output_folder:str=None,
		filename:str=None,
		video_ext:str=None,
		audio_ext:str="mp3",
		add_audio_metadata:bool=True,
		on_progress=None,
		ffmpeg_progress=None,
		on_abort=None,
		on_success=None
	) -> str:
		extension = (self.videoStream and self.videoStream.videoExt) or (self.audioStream and self.audioStream.audioExt)
		target_ext = video_ext or extension if self.videoStream else audio_ext or extension
		target_filename = filename or self.metadata.get("title", "")
		target_filepath = get_file_path(
			filename=target_filename, prefix=target_ext, folder=output_folder
		)
		self.reserve_file(target_filepath)
		on_progress = on_progress or self._default_progress
		ffmpeg_progress = ffmpeg_progress or self._default_progress

		def on_finish(f):
			if on_success: on_success(f)
			return f


		if self.videoStream and self.audioStream:
			filesize = self.videoStream.filesize + self.audioStream.filesize

			async def handle_progress(current, total, base_size=0):
				await on_progress(base_size+current, filesize)

			video_temp = tempfile.TemporaryFile(delete=False).name
			audio_temp = tempfile.TemporaryFile(delete=False).name

			await self._download_stream(self.videoStream.url, video_temp, lambda c,t: handle_progress(c,t))
			await self._download_stream(self.audioStream.url, audio_temp, lambda c,t: handle_progress(c,t,self.videoStream.filesize))
			await self._mix(video_temp, audio_temp, target_filepath, ffmpeg_progress)

			self.remove_file(video_temp)
			self.remove_file(audio_temp)


		elif self.videoStream:
			video_temp = tempfile.TemporaryFile(delete=False).name
			await self._download_stream(self.videoStream.url, video_temp, on_progress)
			if extension == target_ext:
				os.replace(video_temp, target_filepath)
			else:
				await self._convert(video_temp, target_filepath, ffmpeg_progress)

			self.remove_file(video_temp)


		elif self.audioStream:
			audio_temp = tempfile.TemporaryFile(delete=False).name
			await self._download_stream(self.audioStream.url, audio_temp, on_progress)
			if extension == target_ext and not add_audio_metadata:
				os.replace(audio_temp, target_filepath)
			else:
				await self._convert(audio_temp, target_filepath, ffmpeg_progress, (self.metadata if add_audio_metadata else None))

			self.remove_file(audio_temp)

		if self.can_download: return on_finish(target_filepath)
		self.remove_file(target_filepath)
		if on_abort: on_abort()


	async def _mix(self, video, audio, target, progress=None):
		self.remove_file(target)
		if not self.can_download: return
		codecs = ["-c:v", "copy"]
		if target.endswith(".mp4") or target.endswith(".m4a"):
			codecs.extend(["-c:a", "libmp3lame"])
		await self._ffmpeg(["-i", video, "-i", audio, *codecs, target], progress)


	async def _convert(self, inputFile, output, progress=None, metadata=None):
		self.remove_file(output)
		if not self.can_download: return
		codecs = []
		need_detele_thrumb = False
		if output.endswith(".mp3"):
			if metadata:
				if metadata.get('thumbnail'):
					thumb = metadata.get('thumbnail').temp
					need_detele_thrumb = True
					codecs.extend(["-i", thumb, "-map", "0:0", "-map", "1:0"])
				codecs.extend(["-ar", "48000", "-b:a", "192k"])
				if metadata.get('title'):
					title = metadata.get('title').replace('"', '')
					codecs.extend(["-metadata", f"title={title}"])
				if metadata.get('author'):
					artist = metadata.get('author').replace('"', '')
					codecs.extend(["-metadata", f"artist={artist}"])
				codecs.extend(["-id3v2_version", "3"])
				
		await self._ffmpeg(["-i", inputFile, *codecs, output], progress)
		if need_detele_thrumb: os.remove(thumb)


	async def _download_stream(self, url, filename, on_progress=None):
		if not self.can_download: return
		on_progress = on_progress or self._default_progress
		async with aiohttp.ClientSession(headers=self.HEADERS) as session:
			resp_head = await session.get(url)
			file_size = int(resp_head.headers.get('Content-Length'))
			downloaded = 0
			await on_progress(downloaded, file_size)
			with open(filename, "wb") as file:
				while downloaded < file_size:
					if self.can_download:
						stop_pos = min(downloaded + self.CHUNK_SIZE, file_size) - 1
						chunk = await self._make_request(session, url+f"&range={downloaded}-{stop_pos}")
						if not chunk: break
						file.write(chunk)
						downloaded += len(chunk)
						await on_progress(downloaded, file_size)
					else: break

	async def _make_request(self, session, url, retries=3):
		for attempt in range(retries):
			try:
				resp = await session.get(url)
				chunk = await resp.content.read()
				return chunk
			except aiohttp.ClientPayloadError as e:
				if attempt == retries - 1:
					raise e


	async def _ffmpeg(self, command, on_progress=None):
		on_progress = on_progress or self._default_progress
		total_duration = 0
		if not self.can_download: return 1
		process = subprocess.Popen([self.FFMPEG, "-hide_banner"] + command, encoding='utf-8', universal_newlines=True, startupinfo=self.startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		with process.stdout as pipe:
			history = []
			for raw_line in pipe:
				if not self.can_download:
					process.terminate()
					process.wait()
					return 1
				line = raw_line.strip()
				history.append(line)
				if total_duration == 0:
					if "Duration:" in line:
						match = self._DURATION_REG.search(line)
						total_duration = to_seconds(match.groupdict())
						await on_progress(0, total_duration)
				else:
					if "time=" in line:
						match = self._TIME_REG.search(line)
						if match:
							current = to_seconds(match.groupdict())
							await on_progress(current, total_duration)
		process.wait()
		if process.returncode != 0:
			print("\n".join(history))
			raise RuntimeError(f"FFMPEG error occurred: [{history[-1]}]")
		return process.returncode
