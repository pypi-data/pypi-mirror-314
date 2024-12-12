from setuptools import setup, find_packages

VERSION = '0.0.68'
DESCRIPTION = 'Youtube Autonomous main software.'
LONG_DESCRIPTION = 'This is the main Youtube Autonomous project handler, containing the whole functionality.'

setup(
        name = "youtube-autonomous", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'yta-multimedia',
            'yta-general-utils',
            'youtubeenhanced',
            'yta-stock-downloader'
        ],
        
        keywords = [
            'youtube autonomous main software'
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