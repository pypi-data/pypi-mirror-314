from setuptools import setup, find_packages

setup (
    name="fpkws",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    author="FanPars",
    description="Spotting keywords in audio files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)

