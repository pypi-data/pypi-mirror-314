from setuptools import setup


setup(
    name="hyperion-stream-client",
    version="1.0.0",
    author="Uche David",
    author_email="alts.devs@gmail.com",
    description="Streaming Client for Hyperion History API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=["requests", "python-socketio[asyncio_client]", "loguru"],
    url="https://github.com/debugtitan/hyperion-stream-client.git",
    packages=["hyperion"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
