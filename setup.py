from setuptools import setup, find_packages

setup(
    name='ws-cli',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'ws = ws.ws:main',
        ],
    },
)

