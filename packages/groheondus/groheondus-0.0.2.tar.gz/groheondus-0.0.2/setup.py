import setuptools

setuptools.setup(
    name="groheondus",
    version="0.0.2",
    description="Grohe Ondus",
    long_description="""
        With this Python module you can read data from Grohe Ondus""",
    url="http://https://github.com/weaseel/groheondus",
    author="hendrikb",
    author_email="groheondus@hendrik-b.de",
    license="APACHE",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "bs4"
    ],
)