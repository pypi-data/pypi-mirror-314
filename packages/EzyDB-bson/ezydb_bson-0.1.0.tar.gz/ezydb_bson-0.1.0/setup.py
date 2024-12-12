from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EzyDB_bson",
    version="0.1.0",
    description="EzyDB-bson is a lightweight, file-based NoSQL database system designed for Python developers. Plugin for EzyDB.",
    author="Rakesh Kanna",
    author_email='rakeshkanna0108@gmail.com',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['database', 'db', 'nosql', 'bson', 'storage', 'store'],
    install_requires=
        ['textPlay', 'EzyDB', 'click'],
    entry_points={"console_scripts":["EzyDB-bson = EzyDB_bson:main"]}
)
