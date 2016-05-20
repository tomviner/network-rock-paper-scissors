from setuptools import setup

setup(
    name="netrps",
    version="0.0.1",
    author="Tom Viner",
    author_email="netrps@viner.tv",
    description=(
        "A game of Rock, Paper, Scissors over NetworkZero - Trust No One."),
    license="BSD",
    keywords="NetworkZero",
    url="https://github.com/tomviner/network-rock-paper-scissors",
    packages=[
        'netrps'
    ],
    install_requires=[
        'enum34',
        'networkzero',
        'clint',
        'click',
        'six',
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts': [
            'player_one = netrps.game:player_one',
            'player_two = netrps.game:player_two',
        ],
    },
)
