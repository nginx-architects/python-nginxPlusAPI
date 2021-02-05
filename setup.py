import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nginxPlusAPI", # Replace with your own username
    version="0.0.1",
    author="James Jones",
    author_email="jam.jones@f5.com",
    description="Python API Client for NGINX Plus API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nginx-architects/python-nginxPlusAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)