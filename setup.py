from setuptools import setup

setup(
    name="netrps",
    version="0.0.1",
    author="Tom Viner",
    author_email="netrps@viner.tv",
    description=(
        "A game of Rock, Paper, Scissors over NetworkZero - trust no one."),
    license="BSD",
    keywords="NetworkZero",
    url="https://github.com/tomviner/network-rock-paper-scissors",
    pymodules=[
        'rps.py'
        'game.py'
    ],
    install_requires=[
        'enum34',
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
