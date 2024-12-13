from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Google API services simplified.'
LONG_DESCRIPTION = 'A library to simplify the interaction with the Google API services.'

setup(
        name = "yta-google-api", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'google-auth',
            'yta_general_utils',
        ],
        
        keywords = [
            'youtube autonomous google api services',
            'yta google api'
        ],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)