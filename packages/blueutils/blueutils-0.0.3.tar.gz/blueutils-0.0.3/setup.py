import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
project_urls = {
  'Source': 'https://github.com/ox-blueblue/blueutils'
}
setuptools.setup(
    name="blueutils",
    version="0.0.3",
    author="blue",
    author_email="embzhengblue@gmail.com",
    description="This is a crypto operation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ox-blueblue/blueutils",
    packages=setuptools.find_packages(),
    install_requires=['requests'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = project_urls
)