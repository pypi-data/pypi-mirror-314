import pathlib
import re
import setuptools


setuptools.setup(
    name='mindpark',
    version='1.0.0',
    description='Testbed for deep reinforcement learning',
    url='http://github.com/danijar/mindpark',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['mindpark'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
