from importlib import import_module
from pathlib import Path
from setuptools import setup, find_packages

SRC_ROOT = 'src'
BIN_ROOT = 'bin/'

about = import_module(SRC_ROOT + '.hermes_audio_server.about')

with Path('README.md').open('r') as fh:
    long_description = fh.read()

with Path('requirements.txt').open('r') as fh:
    requirements = fh.read().splitlines()
    requirements = [requirement for requirement in requirements
                    if not requirement.startswith('#')]

binaries = [BIN_ROOT + about.PLAYER, BIN_ROOT + about.RECORDER]

setup(
    name=about.PROJECT,
    version=about.VERSION,
    description=about.DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=about.LICENSE,
    author=about.AUTHOR,
    author_email=about.EMAIL,
    url=about.GITHUB_URL,
    project_urls={
        'Documentation': about.DOC_URL,
        'Source': about.GITHUB_URL,
        'Tracker': about.TRACKER_URL,
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
    keywords=about.KEYWORDS,
    scripts=binaries)
