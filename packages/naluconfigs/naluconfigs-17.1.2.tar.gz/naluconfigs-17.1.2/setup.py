import os

import setuptools

CURR_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """Get the version string for the package.

    Expects `naluconfigs/_version.py` to contain a variable
    called `__version__`.

    Returns:
        The version string.

    Raises:
        FileNotFoundError if the version file cannot be found.
        OSError if there was a problem opening the version file.
        KeyError if the `__version__` field does not exist in the file.
    """
    version = dict()
    with open(os.path.join(CURR_DIR, "src", "naluconfigs", "_version.py")) as fp:
        exec(fp.read(), version)
        return version["__version__"]


setuptools.setup(
    name="naluconfigs",
    version=get_version(),
    author="Mitchell Matsumori-Kelly",
    author_email="mitchell@naluscientific.com",
    description="Home for board configs",
    python_requires=">=3.7",
    url="",
    install_requires=[
        "pyyaml>=5.1.1",
        "numpy",
    ],
    tests_require=[
        "pytest>=5.0.1",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "": ["data/clocks/*.txt", "data/registers/*.yml"],
    },
)
