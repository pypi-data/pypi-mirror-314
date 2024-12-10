import setuptools


_ENCODING_UTF8 = "utf-8"
_MODE_R = "r"

_NEW_LINE = "\n"


def _make_descriptions():
	with open("README.md", _MODE_R, encoding=_ENCODING_UTF8) as readme_file:
		readme_content = readme_file.read()

	fr_title = "## FRANÇAIS"
	en_title = "## ENGLISH"

	fr_index = readme_content.index(fr_title)
	fr_dependencies_index = readme_content.index("### Dépendances")

	en_index = readme_content.index(en_title)
	en_desc_index = en_index + len(en_title)
	en_content_index = readme_content.index("### Content", en_desc_index)
	en_dependencies_index = readme_content.index("### Dependencies", en_index)

	short_description = readme_content[en_desc_index: en_content_index]
	short_description = short_description.replace(_NEW_LINE, " ")
	short_description = short_description.replace("`", "")
	short_description = short_description.strip()

	long_description = readme_content[fr_index: fr_dependencies_index]\
		+ readme_content[en_index:en_dependencies_index].rstrip()

	return short_description, long_description


def _make_requirement_list():
	with open("requirements.txt",
			_MODE_R, encoding=_ENCODING_UTF8) as req_file:
		req_str = req_file.read()

	raw_requirements = req_str.split(_NEW_LINE)

	requirements = list()
	for requirement in raw_requirements:
		if len(requirement) > 0:
			requirements.append(requirement)

	return requirements


if __name__ == "__main__":
	short_desc, long_desc = _make_descriptions()

	setuptools.setup(
		name = "repr_rw",
		version = "1.0.6",
		author = "Guyllaume Rousseau",
		description = short_desc,
		long_description = long_desc,
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/repr_rw",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		install_requires = _make_requirement_list(),
		packages = setuptools.find_packages(exclude=("demos", "demo_package",)),
		license = "MIT",
		license_files = ("LICENSE",))
