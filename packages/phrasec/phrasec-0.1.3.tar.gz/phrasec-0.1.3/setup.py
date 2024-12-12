from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
]

setup(
    name='phrasec',
    version='0.1.3',
    description='PassPhrase generator CLI',
    author='Emil Larsson',
    author_email='emil@wirely.se',
    license='MIT',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),  # Automatically find the PhraseCraft package
    package_data={
        "PhraseCraft": ["eef_wordlist.txt"],  # Include the wordlist file in the package
    },
    install_requires=[
        "Click",  # Dependency for your CLI
    ],
    entry_points={
        'console_scripts': [
            'phrasec=PhraseCraft.phrasec:cli',  # Updated to match the source code directory
        ],
    },
    classifiers=classifiers,
)
