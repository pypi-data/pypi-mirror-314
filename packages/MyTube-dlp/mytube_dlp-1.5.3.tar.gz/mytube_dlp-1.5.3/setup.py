import setuptools
with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='MyTube_dlp',
	version='1.5.3',
	author='Super_Zombi',
	author_email='super.zombi.yt@gmail.com',
	description='Python YouTube Downloader',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/MyTube',
	project_urls={
		'Documentation': 'https://superzombi.github.io/MyTube/',
	},
	packages=['MyTube'],
	install_requires=["aiohttp", "requests", "yt-dlp", "Pillow"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)