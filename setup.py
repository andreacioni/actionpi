import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('requirements_raspberry.txt') as f:
    required += f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="actionpi",
    version="1.1.1",
    author="Andrea Cioni",
    description="Action/Dash camera powered by Raspberry Pi Zero",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreacioni/actionpi",
    packages=setuptools.find_packages(),
    install_requires=[
        required
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
