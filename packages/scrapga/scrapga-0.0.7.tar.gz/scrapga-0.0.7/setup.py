from setuptools import setup

setup(
	name="scrapga",
	version="0.0.7",
	description="GSMArena Scraper",
	author="dow",
	author_email="dow@isdow.com",
	url="https://isdow.com",
	license="MIT",
	python_requires=">=3.6",
	install_requires=["beautifulsoup4", "requests"],
	packages=["scrapga"]
)