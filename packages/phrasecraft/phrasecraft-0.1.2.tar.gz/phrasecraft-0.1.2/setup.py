from setuptools import setup

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
]

setup(
    name='phrasecraft',
    version='0.1.2',
    description='PassPhrase generator CLI',
    author='Emil Larsson',
    author_email='emil@wirely.se',
    license='MIT',
    readme = "README.md",
    include_package_data=True,
    py_modules=['generator'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'phrasec = phrasec:cli',
        ],
    },
    classifiers=classifiers,
)