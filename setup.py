from setuptools import setup, find_packages




def find_package_data(start_dir):
    package_data = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            path = os.path.relpath(os.path.join(root, file), start_dir)
            package_data.append(path)
    return package_data

setup(
    name='ws-cli',
    version='1.0',
    packages=find_packages(),
    package_data={
        'ws': find_package_data('ws/')
    },
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

