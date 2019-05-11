from pathlib import Path
from setuptools import setup, find_packages


SRC_ROOT = 'src'
BIN_ROOT = 'bin/'

# Read some information about the project from __about__.py
with (Path(SRC_ROOT) / 'hermes_audio_server' / '__about__.py').open('r') as fh:
    about = dict()
    exec(fh.read(), about)

with Path('README.md').open('r') as fh:
    long_description = fh.read()

with Path('requirements.txt').open('r') as fh:
    requirements = fh.read().splitlines()
    requirements = [requirement for requirement in requirements
                    if not requirement.startswith('#')]

binaries = [BIN_ROOT + about['__player__'], BIN_ROOT + about['__recorder__']]

setup(
    name=about['__project__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__github_url__'],
    project_urls={
        'Documentation': about['__doc_url__'],
        'Source': about['__github_url__'],
        'Tracker': about['__tracker_url__'],
    },
    packages=find_packages(SRC_ROOT),
    package_dir={'': SRC_ROOT},
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Multimedia :: Sound/Audio :: Players'
    ],
    keywords=about['__keywords__'],
    scripts=binaries)
