from setuptools import setup, find_packages
VERSION = "0.0.4"
DESCRIPTION = "Package for User Interface"
LONG_DESCRIPTION = "Package for User Interface"

setup(
    name="UIron",
    version=VERSION,
    author="Armando Chaparro",
    author_email="pylejandria@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['ttkbootstrap'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_data={'': ['data/*']}
)