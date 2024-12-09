import re
import os
import random
import string
from PIL import Image
import requests
import tempfile


class Channel:
	def __init__(self, id:str, url:str, name:str, followers:int=0):
		self.id = id
		self.url = url
		self.followers = followers
		trash = " - Topic"
		self.name = name[:-len(trash)] if name.endswith(trash) else name
	
	def __str__(self): return f'Channel({self.name})'
	def __repr__(self): return str(self)


class Thumbnail:
	def __init__(self, url:str):
		self.url = url
		self._raw = None

	def download(self, folder=None, quality=None):
		if not self._raw: self._parse()
		filepath = get_file_path(random_filename(), "jpg", folder)
		self._save(self._raw, filepath, quality=quality)
		return filepath

	def _save(self, entity, filepath, quality=None):
		options = {
			"max": {"quality": 100, "subsampling": 0},
			"min": {"quality": 90, "optimize": True}
		}
		save_args = options.get(quality, {"quality": 96})
		entity.save(filepath, "JPEG", **save_args)

	def _parse(self):
		img = Image.open(requests.get(self.url, stream=True).raw)
		self._raw = img.convert("RGB")

	@property
	def temp(self):
		if not self._raw: self._parse()
		new_img = self._crop()
		file = tempfile.TemporaryFile(suffix=".jpg", delete=False).name
		self._save(new_img, file)
		return file

	def _crop(self):
		width, height = self._raw.size
		min_side = min(width, height)
		left = (width - min_side) / 2
		top = (height - min_side) / 2
		right = (width + min_side) / 2
		bottom = (height + min_side) / 2
		return self._raw.crop((left, top, right, bottom))

	def __str__(self): return str(self.url)
	def __repr__(self): return 'Thumbnail()'


def random_filename(length=8):
	return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def safe_filename(s:str, max_length:int=255) -> str:
	ntfs_characters = [chr(i) for i in range(0, 31)]
	characters = [r'"',r"\#",r"\$",r"\%",r"'",r"\*",r"\,",r"\.",r"\/",r"\:",r'"',r"\;",r"\<",r"\>",r"\?",r"\\",r"\^",r"\|",r"\~",r"\\\\"]
	pattern = "|".join(ntfs_characters + characters)
	regex = re.compile(pattern, re.UNICODE)
	filename = regex.sub("", s)
	return filename[:max_length].rsplit(" ", 0)[0]

def get_file_path(filename, prefix, folder=""):
	filename = f"{safe_filename(filename)}.{prefix}"
	folder = os.path.abspath(folder) if folder else os.getcwd()
	path = os.path.join(folder, filename)
	os.makedirs(folder, exist_ok=True)
	return file_exists(path)

def file_exists(file:str) -> str:
	if os.path.exists(file):
		name, extension = os.path.splitext(file)

		match = re.search(r'\((\d+)\)$', name)
		if match:
			number = int(match.group(1)) + 1
			new_name = re.sub(r'\(\d+\)$', f'({number})', name)
		else:
			new_name = f"{name} (1)"
		return file_exists(new_name+extension)
	return file

def to_seconds(kwargs: dict) -> int:
	hour = int(kwargs.get("hour", 0))
	minute = int(kwargs.get("min", 0))
	sec = int(kwargs.get("sec", 0))
	return (hour*3600) + (minute*60) + sec

def convert_to_netscape(cookie_data):
	netscape_cookie = "# Netscape HTTP Cookie File\n\n"
	for cookie in cookie_data:
		domain = cookie.get("domain", "")
		name = cookie.get("name", "")
		value = cookie.get("value", "")
		expires = cookie.get("expirationDate", 0)

		netscape_cookie += f"{domain}\tTRUE\t/\tFALSE\t{expires}\t{name}\t{value}\n"
	return netscape_cookie

def get_cookie_file(json_cookies):
	cookies_netscape = convert_to_netscape(json_cookies)
	cookie_file = tempfile.TemporaryFile(suffix=".txt", delete=False).name
	with open(cookie_file, 'w') as f:
		f.write(cookies_netscape)
	return cookie_file
