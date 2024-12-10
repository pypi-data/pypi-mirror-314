import setuptools


def _make_descriptions():
	with open("README.md", "r", encoding="utf-8") as readme_file:
		readme_content = readme_file.read()

	fr_title = "## FRANÇAIS"
	en_title = "## ENGLISH"

	fr_index = readme_content.index(fr_title)
	fr_demo_index = readme_content.index("### Démo")

	en_index = readme_content.index(en_title)
	en_desc_index = en_index + len(en_title)
	en_content_index = readme_content.index("### Content", en_desc_index)
	en_demo_index = readme_content.index("### Demo", en_index)

	short_description = readme_content[en_desc_index: en_content_index]
	short_description = short_description.replace("\n", " ")
	short_description = short_description.replace("`", "")
	short_description = short_description.strip()

	long_description = readme_content[fr_index: fr_demo_index]\
		+ readme_content[en_index:en_demo_index].rstrip()

	return short_description, long_description


if __name__ == "__main__":
	short_desc, long_desc = _make_descriptions()

	setuptools.setup(
		name = "syspathmodif",
		version = "1.1.0",
		author = "Guyllaume Rousseau",
		description = short_desc,
		long_description = long_desc,
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/syspathmodif",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		packages = setuptools.find_packages(
			exclude=(".github", "demo", "demo_package", "tests")),
		license = "MIT",
		license_files = ("LICENSE",))
